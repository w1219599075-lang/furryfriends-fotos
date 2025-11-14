from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Image
from app.forms import RegistrationForm, LoginForm, UploadForm
from app.blob_service import BlobStorageService, allowed_file

def register_routes(app):
    """Register all routes to the application"""
    
    @app.route('/')
    def index():
        """Home page"""
        # If user is already logged in, redirect to gallery
        if current_user.is_authenticated:
            return redirect(url_for('gallery'))
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration"""
        # If already logged in, redirect to home
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = RegistrationForm()
        
        if form.validate_on_submit():
            # Create new user
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            
            # Save to database
            db.session.add(user)
            db.session.commit()

            flash(f'Account created! Welcome, {user.username}', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login"""
        # If already logged in, redirect to home
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        form = LoginForm()
        
        if form.validate_on_submit():
            # Find user
            user = User.query.filter_by(username=form.username.data).first()
            
            # Verify username and password
            if user and user.check_password(form.password.data):
                login_user(user)
                flash(f'Welcome back, {user.username}!', 'success')

                # After successful login, redirect to previous page or gallery
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('gallery'))
            else:
                flash('Wrong username or password', 'danger')
        
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout"""
        try:
            logout_user()
            flash('Logged out successfully', 'info')
        except Exception as e:
            # Log error but still redirect
            print(f"Error during logout: {str(e)}")
            flash('Logged out', 'info')
        return redirect(url_for('index'))

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload():
        """Image upload page"""
        form = UploadForm()

        if form.validate_on_submit():
            try:
                file = form.image.data

                if not allowed_file(file.filename):
                    flash('Invalid file type. Only PNG, JPG, GIF, WebP are allowed.', 'danger')
                    return redirect(url_for('upload'))

                blob_service = BlobStorageService(
                    connection_string=current_app.config['AZURE_STORAGE_CONNECTION_STRING'],
                    container_original=current_app.config['AZURE_STORAGE_CONTAINER_ORIGINAL'],
                    container_thumbnail=current_app.config['AZURE_STORAGE_CONTAINER_THUMBNAIL']
                )

                result = blob_service.upload_file(
                    file_stream=file.stream,
                    original_filename=file.filename,
                    content_type=file.content_type
                )

                if result['success']:
                    download_url = blob_service.generate_download_url(result['blob_name'])

                    new_image = Image(
                        caption=form.caption.data or '',
                        original_url=download_url,
                        user_id=current_user.id
                    )
                    db.session.add(new_image)
                    db.session.commit()

                    flash('Image uploaded successfully! Thumbnail will be generated shortly.', 'success')
                    return redirect(url_for('gallery'))
                else:
                    flash(f'Upload failed: {result.get("error", "Unknown error")}', 'danger')

            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')
                current_app.logger.error(f'Upload error: {str(e)}')

        return render_template('upload.html', form=form)

    @app.route('/gallery')
    def gallery():
        """Public gallery page"""
        images = Image.query.order_by(Image.upload_date.desc()).all()

        blob_service = BlobStorageService(
            connection_string=current_app.config['AZURE_STORAGE_CONNECTION_STRING'],
            container_original=current_app.config['AZURE_STORAGE_CONTAINER_ORIGINAL'],
            container_thumbnail=current_app.config['AZURE_STORAGE_CONTAINER_THUMBNAIL']
        )

        for image in images:
            if image.original_url:
                blob_name = image.original_url.split('/')[-1].split('?')[0]
                thumbnail_url = blob_service.get_thumbnail_url(blob_name)
                image.thumbnail_url = thumbnail_url or image.original_url

        return render_template('gallery.html', images=images)

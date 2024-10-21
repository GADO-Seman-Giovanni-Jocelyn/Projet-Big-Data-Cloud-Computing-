import boto3

def upload_to_s3(file_name, bucket_name, object_name=None):
    # Crée un client S3
    s3 = boto3.client('s3', 
                      aws_access_key_id='VOTRE_ACCESS_KEY',
                      aws_secret_access_key='VOTRE_SECRET_KEY')

    # Définir le nom de l'objet si ce n'est pas spécifié
    if object_name is None:
        object_name = file_name

    # Uploader le fichier sur S3
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        print(f"{file_name} uploadé avec succès dans le bucket {bucket_name}.")
    except Exception as e:
        print(f"Erreur lors de l'upload: {e}")
upload_to_s3('books_scraper.csv', 'nom_du_bucket')
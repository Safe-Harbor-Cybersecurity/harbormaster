# src/harbormaster/cli/commands.py
import click
from harbormaster.core.config import Settings

@click.group()
def cli():
    """Command line interface for Harbormaster
    
    Examples:
        $ harbormaster secure-model bert-base-uncased
        $ harbormaster scan-model gpt2
        $ harbormaster monitor-status
    """
    pass

@cli.command()
@click.argument('model_id')
@click.option('--security-level', default='high', help='Security level (low/medium/high)')
@click.option('--api-key', envvar='HARBORMASTER_API_KEY', help='API key for authentication')
def secure_model(model_id: str, security_level: str, api_key: str):
    """Secure a Hugging Face model with Harbormaster protection.
    
    Args:
        model_id: The Hugging Face model ID to secure
    """
    try:
        # Load settings
        settings = Settings(huggingface_token=api_key)
        
        # Initialize harbor client
        from harbormaster import HarborMaster
        harbor = HarborMaster(api_key=api_key)
        
        # Secure the model
        result = harbor.secure_model(model_id)
        
        click.echo(f"✅ Model {model_id} secured successfully")
        click.echo(f"Security Level: {security_level}")
        click.echo(f"Config: {result['config']}")
        
    except Exception as e:
        click.echo(f"❌ Error securing model: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()
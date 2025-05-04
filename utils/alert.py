def getSuccessAlertScript(message: str, redirect_url) -> str:
    return f"""
    <script>
        $.notify('{message}', 'success');
        setTimeout(() => window.location.href = '{redirect_url}', 2000);
    </script>
    """

def getErrorAlertScript(message: str) -> str:
    return f"""
    <script>
        $.notify('{message}', 'error');
    </script>
    """
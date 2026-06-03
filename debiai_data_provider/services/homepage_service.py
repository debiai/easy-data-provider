from debiai_data_provider.data_provider import DataProvider

def get_homepage_html(data_provider: DataProvider) -> str:
    projects = data_provider.get_projects()
    project_list_html = ""
    for project in projects:
        project_list_html += f"<li>{project.name}</li>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DebiAI Data Provider</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            header {{
                background-color: #4CAF50;
                color: white;
                padding: 1rem;
                text-align: center;
            }}
            main {{
                padding: 1rem;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                background-color: white;
                margin: 0.5rem 0;
                padding: 0.5rem;
                border-radius: 5px;
                box-shadow: 0 0 5px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Welcome to DebiAI Data Provider</h1>
        </header>
        <main>
            <section>
                <h2>About DebiAI</h2>
                <p>DebiAI is a platform for managing and analyzing AI projects.</p>
            </section>
            <section>
                <h2>Provided Projects</h2>
                <ul>
                    {project_list_html}
                </ul>
            </section>
        </main>
    </body>
    </html>
    """
    return html_content

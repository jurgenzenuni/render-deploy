from django.shortcuts import render
from django.db import connection


def index(request):
    role_name = None
    found_username = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        if username:
            # Use parameterized SQL to avoid injection. We assume tables:
            # users(id, user_name, role_id) and roles(role_id, role_name)
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT r.role_name, u.user_name
                    FROM users u
                    JOIN roles r ON r.role_id = u.role_id
                    WHERE u.user_name = %s
                    LIMIT 1
                    """,
                    [username]
                )
                row = cursor.fetchone()
                if row:
                    role_name = row[0]
                    found_username = row[1]
                else:
                    role_name = ''  # indicates not found
                    found_username = ''

    return render(request, 'index.html', {'role_name': role_name, 'found_username': found_username})

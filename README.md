# GhatNiva Properties — Django website

A responsive property website for GhatNiva Properties, focused on plots and duplex homes in Varanasi. The public website uses a custom dark navy and warm gold visual identity with a CSS-built dimensional hero scene. The supplied brand logo is at `static/images/ghatniya-logo.png`.

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt`

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the website and `http://127.0.0.1:8000/admin/` for Django admin.

## Add property listings

Sign into `/admin/`, add a Property, choose Plot or Duplex, fill price, area, location and description, and publish it. Add photos/videos in the inline media section. Choose the cover item and set display order; videos selected as a cover are playable directly from the homepage property card. Enquiries from property detail pages appear in the Enquiries section; change their status and add follow-up notes there.

To preview the site before adding real content, create sample listings:

```powershell
python manage.py seed_demo
```

Sample listings have no fabricated photos; upload real property media through admin.

## Project map

- `config/`: Django configuration and root routes
- `properties/`: Property, media, enquiry models, public views, forms and admin setup
- `templates/`: responsive customer pages and property card
- `static/`: site CSS and supplied logo
- `media/`: uploaded property images/videos (created as needed)
- `db.sqlite3`: local development database (created by `migrate`)

## Deploy on Render

1. Push the project to GitHub and open the [Render Dashboard](https://dashboard.render.com/).
2. Create a PostgreSQL database in Render. Keep it in the same region as the web service.
3. Choose **New > Web Service**, connect `adarshsuraj926499/real-estate-varanasi`, and select the `main` branch.
4. Configure the service:
   - **Language:** Python
   - **Build Command:** `bash build.sh`
   - **Start Command:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
5. Add these environment variables to the web service:
   - `SECRET_KEY`: generate a secret value in Render; never put it in GitHub.
   - `DEBUG`: `False`
   - `DATABASE_URL`: the database's **internal** URL from Render.
   - `ALLOWED_HOSTS`: optional for the Render hostname (it is detected automatically); for a custom domain, add the hostname here.
   - `CSRF_TRUSTED_ORIGINS`: for a custom domain, set its full HTTPS origin, for example `https://www.example.com`.
6. Create the service and wait for the build and deploy to finish. The build collects static files and applies database migrations.
7. Open the service's **Shell** and run `python manage.py createsuperuser`, then visit `/admin/` on the service URL.

Render's default filesystem is temporary. For uploaded property photos and videos to survive deploys, attach a persistent disk to the web service (a paid Render feature), set its mount path to `/var/data`, and add `MEDIA_ROOT=/var/data/media` to the service's environment variables. Re-upload the local video through the live admin after deployment; `media/` and `db.sqlite3` are intentionally not stored in GitHub.

The local development setup continues to use SQLite and the local media directory when the Render environment variables are not set.

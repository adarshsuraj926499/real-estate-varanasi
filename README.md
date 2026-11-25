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

## Deployment notes

Before public deployment, set a strong `SECRET_KEY` through environment variables, set `DEBUG=False`, configure `ALLOWED_HOSTS`, use HTTPS, and move uploaded media to durable object storage. Video file delivery is best served by a media/CDN service.

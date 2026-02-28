# Deploy Sri Amman Jewellery to Render (free, live anywhere)

## 1. Push latest code to GitHub

Already done if you just ran the deploy setup. Your repo: https://github.com/Kalaicharan-M/sri_amman_project

## 2. Create a Render account

- Go to **https://render.com** and sign up (free).
- Use “Sign up with GitHub” and allow access to your repos.

## 3. Deploy the app

1. In Render dashboard click **New +** → **Web Service**.
2. Connect **GitHub** and choose the repo **Kalaicharan-M/sri_amman_project**.
3. Use these settings:
   - **Name:** `sri-amman-jewellery` (or any name)
   - **Region:** Pick the closest to you
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free
4. Click **Create Web Service**.

Render will build and deploy. The first run can take a few minutes.

## 4. Your live URL

When the deploy finishes, you’ll get a URL like:

**https://sri-amman-jewellery.onrender.com**

Share this link to open the site from anywhere.

## 5. Updates

After you change code:

1. Push to GitHub: `git add .` → `git commit -m "Update"` → `git push`
2. Render will redeploy automatically.

---

**Note:** On the free plan, the app may sleep after ~15 minutes of no traffic. The first visit after that can take 30–60 seconds to wake up.

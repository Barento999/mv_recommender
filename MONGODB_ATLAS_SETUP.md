# 🗄️ MongoDB Atlas Setup Guide

## 📍 Get Your Connection String

### Step 1: Go to MongoDB Atlas Dashboard
1. Visit https://www.mongodb.com/cloud/atlas
2. Login to your account
3. Click on your project/cluster

### Step 2: Get Connection String
1. Click **"Connect"** button
2. Choose **"Connect your application"**
3. Select **"Python"** as driver
4. Select **version 4.x**
5. Copy the connection string (looks like this):
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/database_name?retryWrites=true&w=majority
```

### Step 3: Update .env File
Edit `/home/barento/Desktop/reco/backend/.env`:

```bash
# Replace MONGODB_URL with your connection string
MONGODB_URL=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.xxxxx.mongodb.net/movierego?retryWrites=true&w=majority

DATABASE_NAME=movierego
SECRET_KEY=your-secret-key
DEBUG=True
```

**Important:**
- Replace `YOUR_USERNAME` with your MongoDB username
- Replace `YOUR_PASSWORD` with your password (URL encode special chars: @ → %40, # → %23, etc.)
- Replace `YOUR_CLUSTER` with your cluster name
- Keep `movierego` as database name

---

## 🔐 Security Tips

### For Production:
1. **Use environment variables** (`.env` file is NOT committed)
2. **Never hardcode credentials** in source code
3. **IP Whitelist**: Add your IP to MongoDB Atlas IP whitelist
4. **Strong password**: Use 16+ characters with special chars

### For Development:
1. Use a separate MongoDB Atlas cluster
2. Grant limited permissions to your user
3. Use throwaway passwords you don't mind exposing

---

## ✅ Verify Connection

After updating `.env`, start the backend:

```bash
cd backend
./venv/bin/python -m uvicorn app.main:app --reload
```

**Success output:**
```
✓ Connected to MongoDB
INFO:     Application startup complete
```

**If it fails:**
```
✗ Failed to connect to MongoDB: <error>
```

---

## 🚀 Example .env File

```env
# Production Example
MONGODB_URL=mongodb+srv://movieapp_user:SecureP@ssw0rd%40123@movieapp-cluster.a1b2c.mongodb.net/movierego?retryWrites=true&w=majority
DATABASE_NAME=movierego
SECRET_KEY=production-secret-key-min-32-chars-here-12345
DEBUG=False
```

---

## 📝 Complete Setup After .env Update

```bash
# Terminal 1 - Backend
cd backend
./venv/bin/python -m uvicorn app.main:app --reload
# Wait for "Application startup complete"

# Terminal 2 - Set Admin Password
cd backend
./venv/bin/python3 setup_admin.py
# Follow prompts

# Terminal 3 - Frontend
cd frontend
npm run dev

# Browser
# http://localhost:5173
```

---

## ❓ Troubleshooting

### Connection String Format Error
**Problem:** `Invalid URL scheme`
**Solution:**
- Ensure it starts with `mongodb+srv://` (for Atlas)
- Not `mongodb://` (that's for localhost)

### Authentication Failed
**Problem:** `Authentication failed`
**Solution:**
- Verify username and password are correct
- Check URL encoding for special characters (@, #, $, etc.)
- Check IP is whitelisted in MongoDB Atlas

### Database Not Found
**Problem:** Could not connect - database doesn't exist
**Solution:**
- That's OK! MongoDB Atlas creates it on first use
- Just start the backend and it will auto-seed

### Character Encoding Issues
**Problem:** Password with special chars not working
**Solution:**
Use URL encoding:
```
@ → %40
# → %23
$ → %24
: → %3A
/ → %2F
```

Example: `pass@word#123` → `pass%40word%23123`

---

## 🔗 Useful Links

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [Connection String Documentation](https://docs.mongodb.com/manual/reference/connection-string/)
- [MongoDB Atlas IP Whitelist](https://docs.atlas.mongodb.com/security/ip-whitelist/)

---

## ✨ You're Ready!

Once `.env` is updated with your MongoDB Atlas connection string:
1. Start backend - it will auto-seed database
2. Run setup_admin.py - create admin account
3. Start frontend
4. Login and enjoy!

**System will work exactly the same as localhost MongoDB!** 🎉

// Inside your frontend verify.js asset script
const response = await fetch(`${API_BASE_URL}/verify-email?token=${token}`);
const data = await response.json();

if (response.ok) {
    // 🚀 Now your frontend can read the URL string and redirect!
    window.location.href = data.url; 
}
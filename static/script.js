// 1. Elements ko select kar rahe hain (IDs match kar li hain)
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const chatWindow = document.getElementById('chatWindow');
const greetings = document.getElementById('greetings');
let isFirstMessage = true;  // Pehle message par dhyan rakhne ke liye variable

// 2. Message process karne ka main function
function processMessage() {
    const messageText = userInput.value.trim(); // User ka input text

    if (messageText !== "") {
        // --- Greeting Gayab karna ---
        // Jab pehla message aaye toh "Hi Raj..." wala text hamesha ke liye hide kar do
        if (greetings) {
            greetings.style.display = "none";
        }

        // --- AI ka brand name change karna ---
        if (isFirstMessage){
            const brandHeader = document.getElementById("ai-brand-name");
            if (brandHeader) {
                brandHeader.innerText = "Raj-AI";   // Top-left mein jo naam dikhana hai
            }
            isFirstMessage = false; // Flag false kiya taaki agle messages par naam baar-baar na badle
        }

        // --- User ka Question Screen par dikhana ---
        const userMessageDiv = document.createElement('div');
        
        // Styling User Message (Tumhere CSS theme ke hisaab se)
        userMessageDiv.style.alignSelf = "flex-end"; // Right side mein dikhega
        userMessageDiv.style.backgroundColor = "#1e293b"; 
        userMessageDiv.style.color = "#38bdf8"; 
        userMessageDiv.style.padding = "12px 18px";
        userMessageDiv.style.margin = "10px 0";
        userMessageDiv.style.borderRadius = "15px 15px 0 15px";
        userMessageDiv.style.maxWidth = "80%";
        userMessageDiv.style.fontSize = "18px";
        userMessageDiv.style.fontFamily = "Arial, sans-serif";
        userMessageDiv.innerHTML = `<strong>Raj:</strong> ${messageText}`;
        
        // Append: Chat window ke niche joda
        chatWindow.appendChild(userMessageDiv);

        // Input box ko khali (clear) kiya
        userInput.value = "";

        // --- Asli AI ka Response (Flask Backend aur Gemini se) ---
        
        // A. Pehle screen par ek temporary "Thinking..." message dikha dete hain
        const aiMessageDiv = document.createElement('div');
        aiMessageDiv.style.alignSelf = "flex-start"; // Left side mein dikhega
        aiMessageDiv.style.backgroundColor = "transparent";
        aiMessageDiv.style.color = "#ffffff";
        aiMessageDiv.style.padding = "12px 18px";
        aiMessageDiv.style.margin = "10px 0";
        aiMessageDiv.style.fontSize = "18px";
        aiMessageDiv.style.fontFamily = "Arial, sans-serif";
        aiMessageDiv.innerHTML = `<strong style="color: #818cf8;">Raj-AI:</strong> Soch raha hoon...`;
        
        chatWindow.appendChild(aiMessageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll neeche kiya

        // B. Fetch API ka use karke Python backend (/api/chat) ko user ka message bhej rahe hain
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText }) // JSON data bheja
        })
        .then(response => response.json())
        .then(data => {
            // Server se real answer aane par "Soch raha hoon..." ko asli reply se badal diya
            if (data.reply) {
                //aiMessageDiv.innerHTML = `<strong style="color: #818cf8;">Raj-AI:</strong> ${data.reply}`;
                const parsedReply = marked.parse(data.reply);
                aiMessageDiv.innerHTML = `<strong style="color: #818cf8:">Raj-AI:</strong> <div style ="margin-top: 8px;">${parsedReply}</div>`;
            } else {
                aiMessageDiv.innerHTML = `<strong style="color: #818cf8;">Raj-AI:</strong> Sorry bhai, reply nahi mil paya!`;
            }
            chatWindow.scrollTop = chatWindow.scrollHeight; // Dobara auto-scroll kiya
        })
        .catch(error => {
            console.error('Error:', error);
            aiMessageDiv.innerHTML = `<strong style="color: #ef4444;">Raj-AI:</strong> Network error aa gaya bhai!`;
            chatWindow.scrollTop = chatWindow.scrollHeight;
        });
    }
}
// 3.Trigger Points (Events)
sendBtn.addEventListener('click', processMessage);
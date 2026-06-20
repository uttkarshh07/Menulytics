// Function triggered when the user clicks "Find Places"
async function fetchRecommendations() {
    const resultsSection = document.getElementById("results-section");
    const resultsGrid = document.getElementById("results-grid");

    const location = document.getElementById("location").value.trim();
    const budget = document.getElementById("budget").value.trim();
    const people = document.getElementById("people").value.trim();
    const cuisine = document.getElementById("cuisine").value.trim();
    const occasion = document.getElementById("occasion").value.trim();

    let queryParts = [];

    if (cuisine) queryParts.push(cuisine);
    if (occasion) queryParts.push(occasion);
    if (location) queryParts.push(`in ${location}`);
    if (budget) queryParts.push(`under ₹${budget}`);
    if (people) queryParts.push(`for ${people} people`);

    const query = queryParts.join(" ");

    resultsSection.classList.remove("hidden");
    resultsGrid.innerHTML = `
        <p style="text-align:center; width:100%; color: var(--text-light);">
            AI is finding the best restaurants for you...
        </p>
    `;

    resultsSection.scrollIntoView({ behavior: "smooth" });

    try {
        const response = await fetch("http://127.0.0.1:8000/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query || "best restaurants in Indore"
            })
        });

        if (!response.ok) {
            throw new Error("Backend response was not ok");
        }

        const apiResponse = await response.json();

        const recommendations = apiResponse.data.recommendations;

        resultsGrid.innerHTML = "";

        if (!recommendations || recommendations.length === 0) {
            resultsGrid.innerHTML = `
                <p style="text-align:center; width:100%; color: var(--text-light);">
                    No restaurants found. Try changing your budget, cuisine, or location.
                </p>
            `;
            return;
        }

        recommendations.forEach(restaurant => {
            const card = document.createElement("div");
            card.className = "restaurant-card";

            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <h3>${restaurant.restaurant_name}</h3>
                    <div style="font-weight: bold; color: var(--primary-color);">
                        ⭐ ${restaurant.rating}
                    </div>
                </div>

                <p class="rest-location">
                    📍 ${restaurant.area || "Indore"} | 🍽️ ${(restaurant.cuisines || []).join(", ")}
                </p>

                <div class="metrics">
                    <span class="vfm" style="color: #2E7D32;">
                        🔥 Trending Score: ${Number(restaurant.trending_score).toFixed(2)}
                    </span>
                    <span>
                        💰 ₹${restaurant.estimated_cost_for_two} for two
                    </span>
                </div>

                <div class="ai-summary" style="border-left: 4px solid var(--secondary-color); padding-left: 1rem; margin-bottom: 1.5rem;">
                    <p><strong>AI Explanation:</strong></p>
                    <p style="font-size: 0.95rem; margin-top: 0.5rem; color: var(--text-light);">
                        "${restaurant.explanation}"
                    </p>
                </div>

                <div class="card-actions" style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #F5E6D3;">
                    <a href="${restaurant.google_maps_url}" target="_blank" class="map-link" style="color: var(--primary-color); text-decoration: none; font-weight: 600; font-size: 0.9rem;">
                        View on Map
                    </a>
                </div>
            `;

            resultsGrid.appendChild(card);
        });

    } catch (error) {
        console.error("Error fetching recommendations:", error);

        resultsGrid.innerHTML = `
            <p style="color: #FF4757; text-align:center; width:100%; font-weight: bold;">
                Error: Could not connect to AI backend. Make sure FastAPI is running on port 8000.
            </p>
        `;
    }
}

// ==========================================
// Phase 10 / Version 2: Modal Functions
// ==========================================

// Function to open the pop-up on the same page (For Trending Dishes)
function openModal(restaurantName) {
    document.getElementById('modal-title').innerText = restaurantName;
    
    // Hardcoded fake dishes for the visual demo - to be replaced by dynamic data later
    document.getElementById('modal-dishes').innerHTML = `
        <li>Truffle Mushroom Risotto - Highly Positive</li>
        <li>Classic Tiramisu - Positive</li>
    `;
    
    document.getElementById('details-modal').classList.remove('hidden');
}

// Function to close the pop-up
function closeModal() {
    document.getElementById('details-modal').classList.add('hidden');
}
// ==========================================
// Custom Dropdown Logic
// ==========================================

function setupCustomDropdown(displayId, optionsId, inputId) {
    const display = document.getElementById(displayId);
    const optionsMenu = document.getElementById(optionsId);
    const hiddenInput = document.getElementById(inputId);
    const options = optionsMenu.querySelectorAll('.option');

    // Toggle menu open/close
    display.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent document click from closing immediately
        
        // Close all other dropdowns first
        document.querySelectorAll('.custom-options').forEach(menu => {
            if (menu.id !== optionsId) menu.classList.add('hidden');
        });
        document.querySelectorAll('.custom-select').forEach(box => {
            if (box.id !== displayId) box.classList.remove('active');
        });

        optionsMenu.classList.toggle('hidden');
        display.classList.toggle('active');
    });

    // Handle option selection
    options.forEach(option => {
        option.addEventListener('click', () => {
            // Update display text
            display.innerText = option.innerText;
            display.classList.add('has-value'); // Makes text darker
            
            // Update hidden input value for the main JS to read
            hiddenInput.value = option.getAttribute('data-value');
            
            // Close menu
            optionsMenu.classList.add('hidden');
            display.classList.remove('active');
        });
    });
}

// Initialize the dropdowns
setupCustomDropdown('cuisine-display', 'cuisine-options', 'cuisine');
setupCustomDropdown('occasion-display', 'occasion-options', 'occasion');

// Close dropdowns when clicking anywhere outside of them
document.addEventListener('click', () => {
    document.querySelectorAll('.custom-options').forEach(menu => menu.classList.add('hidden'));
    document.querySelectorAll('.custom-select').forEach(box => box.classList.remove('active'));
});
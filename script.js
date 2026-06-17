// Function triggered when the user clicks "Find Places"
async function fetchRecommendations() {
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    
    // Show the results section and add a loading message
    resultsSection.classList.remove('hidden');
    resultsGrid.innerHTML = '<p style="text-align:center; width:100%; color: var(--text-light);">🧠 AI is analyzing reviews, menus, and prices...</p>';
    
    // Smooth scroll down to the results area
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    try {
        // Simulate a slight AI processing delay for realistic UX
        await new Promise(resolve => setTimeout(resolve, 800));

        // Fetch the mock data (acting as our backend for now)
        const response = await fetch('mock-data.json');
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Clear the loading text
        resultsGrid.innerHTML = '';

        // Check if there are no results (Empty State handling)
        if (!data.restaurants || data.restaurants.length === 0) {
            resultsGrid.innerHTML = `<p style="text-align:center; width:100%; color: var(--text-light);">
                Oops! We couldn't find any restaurants matching those exact criteria. Try adjusting your budget or location.
            </p>`;
            return;
        }

        // Loop through the JSON data and build a card for each restaurant
        data.restaurants.forEach(restaurant => {
            const card = document.createElement('div');
            card.className = 'restaurant-card';
            
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <h3>${restaurant.name}</h3>
                    <div style="font-weight: bold; color: var(--primary-color);">⭐ ${restaurant.ai_analytics.overall_rating}</div>
                </div>
                <p class="rest-location">📍 ${restaurant.location_details.area}, ${restaurant.location_details.city} | 🍽️ ${restaurant.cuisines.join(', ')}</p>
                
                <div class="metrics">
                    <span class="vfm" style="color: #2E7D32;">🎯 VFM Score: ${restaurant.ai_analytics.value_score}/100</span>
                    <span>💰 ₹${restaurant.average_cost_for_two} for two</span>
                </div>
                
                <div class="ai-summary" style="border-left: 4px solid var(--secondary-color); padding-left: 1rem; margin-bottom: 1.5rem;">
                    <p><strong>🤖 AI Explanation:</strong></p>
                    <p style="font-size: 0.95rem; margin-top: 0.5rem; color: var(--text-light);">
                        "${restaurant.review_intelligence.nlp_summary}"
                    </p>
                </div>

                <div class="card-actions" style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #F5E6D3;">
                    <a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(restaurant.name + ' ' + restaurant.location_details.area + ' ' + restaurant.location_details.city)}" target="_blank" class="map-link" style="color: var(--primary-color); text-decoration: none; font-weight: 600; font-size: 0.9rem;">
                        🗺️ View on Map
                    </a>
                    <div class="user-interactions" style="display: flex; gap: 10px;">
                        <button class="icon-btn" title="Like this recommendation" onclick="this.classList.toggle('liked')" style="background: none; border: 1px solid #DABBA6; border-radius: 50%; width: 35px; height: 35px; cursor: pointer;">❤️</button>
                        <button class="icon-btn" title="Accurate AI recommendation" style="background: none; border: 1px solid #DABBA6; border-radius: 50%; width: 35px; height: 35px; cursor: pointer;">👍</button>
                        <button class="icon-btn" title="Inaccurate AI recommendation" style="background: none; border: 1px solid #DABBA6; border-radius: 50%; width: 35px; height: 35px; cursor: pointer;">👎</button>
                    </div>
                </div>
            `;
            
            resultsGrid.appendChild(card);
        });

    } catch (error) {
        console.error("Error fetching data:", error);
        resultsGrid.innerHTML = `<p style="color: #FF4757; text-align:center; width:100%; font-weight: bold;">
            Error: Could not load data. Ensure your local server is running so the fetch API can access the backend.
        </p>`;
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
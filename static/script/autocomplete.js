document.addEventListener("DOMContentLoaded", () => {
    const itemInput = document.getElementById("item");
    const suggestionsBox = document.getElementById("item-suggestions");

    // Fetch the custom dataset from an external JSON file
    fetch("static/json/items.json")
        .then(response => response.json())
        .then(items => {
            const itemsDataset = items.map(item => item.name);

            itemInput.addEventListener("input", () => {
                const query = itemInput.value.toLowerCase();
                suggestionsBox.innerHTML = "";  // Clear existing suggestions

                if (query) {
                    const filteredItems = itemsDataset.filter(item =>
                        item.toLowerCase().startsWith(query)
                    );

                    if (filteredItems.length) {
                        suggestionsBox.style.display = "block";
                        filteredItems.forEach(item => {
                            const suggestion = document.createElement("div");
                            suggestion.textContent = item;
                            suggestion.addEventListener("click", () => {
                                itemInput.value = item;
                                suggestionsBox.style.display = "none";
                            });
                            suggestionsBox.appendChild(suggestion);
                        });
                    } else {
                        suggestionsBox.style.display = "none";
                    }
                } else {
                    suggestionsBox.style.display = "none";
                }
            });

            // Hide suggestions box if clicked outside
            document.addEventListener("click", (e) => {
                if (!suggestionsBox.contains(e.target) && e.target !== itemInput) {
                    suggestionsBox.style.display = "none";
                }
            });
        })
        .catch(error => {
            console.error("Error loading dataset:", error);
        });
});

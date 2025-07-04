const textDiv = document.getElementById("list-task-items");
const addButton = document.getElementById("add");
const updateButton = document.getElementById("update");
const deleteButton = document.getElementById("delete");
const inputField = document.getElementById("addTaskField");

let selectedTaskId = null;

// Load all items on page load
window.onload = fetchItems;

// Fetch and display tasks
function fetchItems() {
    fetch("http://localhost:8000/items")
        .then(response => response.json())
        .then(data => {
            textDiv.innerHTML = "";
            data.forEach(item => {
                const itemDiv = document.createElement("li");
                itemDiv.textContent = `${item.name}`;
                itemDiv.dataset.id = item.id;
                itemDiv.dataset.name = item.name;
                itemDiv.classList.add("task-item");

                itemDiv.addEventListener("click", () => {
                    selectTask(item.id, item.name);
                });

                textDiv.appendChild(itemDiv);
            });
        })
        .catch(error => {
            console.error("Error fetching items:", error);
            textDiv.innerText = "Failed to load tasks.";
        });
}

// Select a task by ID
function selectTask(id, name) {
    selectedTaskId = id;
    inputField.value = name;

    // Highlight selected
    const allItems = document.querySelectorAll(".task-item");
    allItems.forEach(el => el.classList.remove("selected"));
    const selected = Array.from(allItems).find(el => el.dataset.id == id);
    if (selected) selected.classList.add("selected");
}

// Add a new task
addButton.addEventListener("click", () => {
    const taskName = inputField.value.trim();
    if (!taskName) return alert("Please enter a task name.");

    fetch("http://localhost:8000/create_items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: taskName })
    })
    .then(() => {
        inputField.value = "";
        selectedTaskId = null;
        fetchItems();
    })
    .catch(error => console.error("Error adding item:", error));
});

// Update selected task
updateButton.addEventListener("click", () => {
    const taskName = inputField.value.trim();
    if (!taskName || selectedTaskId === null) return alert("You need to select any one task to perform this action");

    fetch(`http://localhost:8000/update_items/${selectedTaskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: taskName })
    })
    .then(() => {
        inputField.value = "";
        selectedTaskId = null;
        fetchItems();
    })
    .catch(error => console.error("Error updating item:", error));
});

// Delete selected task
deleteButton.addEventListener("click", () => {
    if (selectedTaskId === null) return alert("You need to select any one task to perform this action");

    fetch(`http://localhost:8000/remove_items/${selectedTaskId}`, {
        method: "DELETE"
    })
    .then(() => {
        inputField.value = "";
        selectedTaskId = null;
        fetchItems();
    })
    .catch(error => console.error("Error deleting item:", error));
});

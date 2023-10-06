const addTaskButton = document.getElementById("addTask");
const removeTaskButton = document.getElementById("removeTask");
const clearCompletedTaskButton = document.getElementById("clearCompleted");
const taskList = document.getElementById("taskList");
const taskInput = document.getElementById("taskInput");
const todoContainer = document.getElementById("todoContainer");

const noTasksMessage = document.createElement("div");
noTasksMessage.innerHTML = "No todos to do";
noTasksMessage.classList.add("no-tasks-message");

window.addEventListener("load", () => {
	const storedTasks = JSON.parse(localStorage.getItem("tasks")) || [];

	storedTasks.forEach((storedTask) => {
		addTask(storedTask.text);
	});
});

function addTask(taskText) {
	if (taskText !== "") {
		const taskItem = document.createElement("div");

		const taskCheckBox = document.createElement("input");
		taskCheckBox.type = "checkbox";
		taskCheckBox.classList.add("task-checkbox");
		taskItem.appendChild(taskCheckBox);

		const taskTextSpan = document.createElement("span");
		taskTextSpan.textContent = taskText;
		taskTextSpan.classList.add("task-text");
		taskItem.appendChild(taskTextSpan);

		taskCheckBox.addEventListener("change", () => {
			taskTextSpan.classList.toggle("completed", taskCheckBox.checked);
		});

		// Create a container for the buttons
		const buttonsContainer = document.createElement("div");
		buttonsContainer.classList.add("task-buttons-container");

		const removeButton = document.createElement("button");
		removeButton.type = "button";

		// Create the Font Awesome icon element
		const removeIcon = document.createElement("i");
		removeIcon.classList.add("fa-solid", "fa-trash");
		removeIcon.style.color = "#dee2e8";

		// Append the icon to the button
		removeButton.appendChild(removeIcon);
		removeButton.classList.add("task-button");
		removeButton.addEventListener("click", () => {
			// Select the corresponding task item for removal
			taskList.removeChild(taskItem);
			updateTaskListVisibility();
			saveToLocalStorage();
		});
		buttonsContainer.appendChild(removeButton);

		const editButton = document.createElement("button");
		editButton.type = "button";

		// Create the Font Awesome icon element
		const editIcon = document.createElement("i");
		editIcon.classList.add("fa-regular", "fa-pen-to-square");
		editIcon.style.color = "#e8e8e9";

		// Append the icon to the button
		editButton.appendChild(editIcon);
		editButton.classList.add("task-button");
		editButton.addEventListener("click", () => {
			const newTaskText = prompt("Edit the task:", task.text);
			if (newTaskText !== null) {
				taskTextSpan.textContent = newTaskText;
			}
		});
		buttonsContainer.appendChild(editButton);

		taskItem.appendChild(buttonsContainer);
		taskItem.classList.add("task-item");
		taskList.appendChild(taskItem);

		taskInput.value = "";

		updateTaskListVisibility();
		saveToLocalStorage();
	}
}

addTaskButton.addEventListener("click", () => {
	const taskText = taskInput.value.trim();
	addTask(taskText);
});

taskInput.addEventListener("keyup", (event) => {
	if (event.key === "Enter") {
		const taskText = taskInput.value.trim();
		addTask(taskText);
	}
});

function clearCompletedTasks() {
	const completedTasks = document.querySelectorAll(".completed");
	completedTasks.forEach((taskCheckBox) => {
		const taskItem = taskCheckBox.parentElement;
		taskList.removeChild(taskItem);
	});

	updateTaskListVisibility();
	saveToLocalStorage();
}

clearCompletedTaskButton.addEventListener("click", clearCompletedTasks);

// Function to update task list visibility based on the number of tasks
function updateTaskListVisibility() {
	if (taskList.children.length === 0) {
		taskList.style.display = "none";
		if (!todoContainer.contains(noTasksMessage)) {
			todoContainer.insertBefore(noTasksMessage, todoContainer.firstChild);
		}
	} else {
		taskList.style.display = "block";
		if (todoContainer.contains(noTasksMessage)) {
			todoContainer.removeChild(noTasksMessage);
		}
	}
}

// Initial check for task list visibility
updateTaskListVisibility();

function saveToLocalStorage() {
	const tasks = Array.from(document.querySelectorAll(".task-item")).map(
		(taskItem) => ({
			text: taskItem.querySelector("span").textContent,
			completed: taskItem.querySelector("input[type='checkbox']").checked,
		})
	);
	localStorage.setItem("tasks", JSON.stringify(tasks));
}

function getCSRFToken() {
	const name = "csrftoken=";
	const cookieArray = document.cookie.split(";");
	for (let i = 0; i < cookieArray.length; i++) {
		let cookie = cookieArray[i].trim();
		if (cookie.indexOf(name) === 0) {
			return cookie.substring(name.length, cookie.length);
		}
	}
	return null; // If CSRF token is not found
}

function updateTaskStatus(selectElement) {
	const taskId = selectElement.getAttribute("data-task-id");
	const newStatus = selectElement.value;

	const csrfToken = getCSRFToken(); // Get the CSRF token

	fetch(`/tasks/update_status/${taskId}/`, {
		method: "POST",
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
			"X-CSRFToken": csrfToken, // Use the retrieved CSRF token
		},
		body: `status=${newStatus}`,
	})
		.then((response) => response.json())
		.then((data) => {
			console.log(data.message);
		});
}

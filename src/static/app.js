document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const template = document.getElementById("activity-card-template");
  
  // Function to remove a participant from an activity
  async function removeParticipant(activityName, email) {
    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: 'DELETE',
        }
      );

      const result = await response.json();

      if (response.ok) {
        // Show success message
        messageDiv.textContent = `${email} has been removed from ${activityName}`;
        messageDiv.className = 'success';
        messageDiv.classList.remove('hidden');
        
        // Hide message after 3 seconds
        setTimeout(() => {
          messageDiv.classList.add('hidden');
        }, 3000);

        // Reload activities list
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || 'Failed to remove participant';
        messageDiv.className = 'error';
        messageDiv.classList.remove('hidden');
        
        setTimeout(() => {
          messageDiv.classList.add('hidden');
        }, 5000);
      }
    } catch (error) {
      messageDiv.textContent = 'Failed to remove participant. Please try again.';
      messageDiv.className = 'error';
      messageDiv.classList.remove('hidden');
      console.error('Error removing participant:', error);
      
      setTimeout(() => {
        messageDiv.classList.add('hidden');
      }, 5000);
    }
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        // Clone the template
        const activityCard = template.content.cloneNode(true);

        // Populate card content
        activityCard.querySelector('.activity-name').textContent = name;
        activityCard.querySelector('.activity-description').textContent = details.description;
        activityCard.querySelector('.activity-schedule').textContent = details.schedule;

        // Populate participants list
        const participantsList = activityCard.querySelector('.participants-list');
        participantsList.innerHTML = '';
        
        if (details.participants && details.participants.length > 0) {
          details.participants.forEach(email => {
            const li = document.createElement('li');
            li.className = 'participant-item';
            
            const participantText = document.createElement('span');
            participantText.textContent = email;
            participantText.className = 'participant-email';
            
            const deleteIcon = document.createElement('button');
            deleteIcon.innerHTML = '🗑️';
            deleteIcon.className = 'delete-participant';
            deleteIcon.title = `Remove ${email} from ${name}`;
            deleteIcon.onclick = () => {
              if (confirm(`Are you sure you want to remove ${email} from ${name}?`)) {
                removeParticipant(name, email);
              }
            };
            
            li.appendChild(participantText);
            li.appendChild(deleteIcon);
            participantsList.appendChild(li);
          });
        } else {
          const li = document.createElement('li');
          li.textContent = 'No participants yet';
          li.style.color = '#999';
          li.style.fontStyle = 'italic';
          li.className = 'no-participants';
          participantsList.appendChild(li);
        }

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;
    const messageDiv = document.getElementById("message");

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);

      // Reload activities list
      fetchActivities();
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});

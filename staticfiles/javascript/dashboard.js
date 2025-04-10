document.addEventListener("DOMContentLoaded", function() {
    // Ensure canvas elements exist
    if (document.getElementById('taskBarChart') && document.getElementById('taskPieChart')) {
        
        const totalTasks = {{ total_tasks|default:"0" }};
        const completedTasks = {{ tasks_completed|default:"0" }};
        const upcomingEvents = {{ upcoming_events|default:"0" }};
        const teamMembers = {{ team_members|default:"0" }};
        const remainingTasks = totalTasks - completedTasks;

        // Bar Chart for Task Statistics
        const taskBarChartCtx = document.getElementById('taskBarChart').getContext('2d');
        new Chart(taskBarChartCtx, {
            type: 'bar',
            data: {
                labels: ['Total Tasks', 'Completed Tasks', 'Upcoming Events', 'Team Members'],
                datasets: [{
                    label: 'Task Statistics',
                    data: [totalTasks, completedTasks, upcomingEvents, teamMembers],
                    backgroundColor: ['#007BFF', '#28a745', '#ffc107', '#6c757d'],
                    borderColor: ['#0056b3', '#218838', '#e0a800', '#5a6268'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Pie Chart for Task Distribution (Completed vs Remaining)
        const taskPieChartCtx = document.getElementById('taskPieChart').getContext('2d');
        new Chart(taskPieChartCtx, {
            type: 'pie',
            data: {
                labels: ['Completed Tasks', 'Remaining Tasks'],
                datasets: [{
                    label: 'Task Completion',
                    data: [completedTasks, remainingTasks],
                    backgroundColor: ['#28a745', '#ffc107'],
                    borderColor: ['#218838', '#e0a800'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true
            }
        });

    } else {
        console.warn("Chart canvas elements not found!");
    }
});
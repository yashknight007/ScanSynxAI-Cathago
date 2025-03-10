document.addEventListener('DOMContentLoaded', () => {
    const fetchAnalytics = async () => {
        try {
            const response = await fetch('/admin/analytics/');
            const data = await response.json();
            updateAnalytics(data.analytics);
        } catch (error) {
            console.error('Error fetching analytics:', error);
        }
    };

    const updateAnalytics = (analytics) => {
        // Update stat cards
        document.getElementById('totalUsers').textContent = analytics.total_users;
        document.getElementById('totalDocuments').textContent = analytics.total_documents_uploaded;
        document.getElementById('totalCreditRequests').textContent = analytics.total_credit_requests;
        document.getElementById('approvedRequests').textContent = analytics.approved_credit_requests;

        // Update Scans per Day Chart
        updateScansChart(analytics.scans_per_day);

        // Update Most Common Document Topics
        updateCommonTopics(analytics.common_topics);

        // Update Top Users by Scans
        updateList("topUserScans", analytics.top_users_by_scans);

        // Update Credit Usage Statistics
        updateList("creditUsage", analytics.credit_usage);

        // Animate counters
        animateCounters();
    };

    const updateScansChart = (scansData) => {
        const ctx = document.getElementById('userGrowthChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: Object.keys(scansData), // Dates
                datasets: [{
                    label: 'Scans per Day',
                    data: Object.values(scansData), // Scan counts
                    borderColor: 'blue',
                    borderWidth: 2
                }]
            }
        });
    };

    const updateCommonTopics = (topicsData) => {
        const topicList = document.getElementById('commonTopics');
        topicList.innerHTML = "";
        for (const [topic, count] of Object.entries(topicsData)) {
            const listItem = document.createElement('li');
            listItem.textContent = `${topic}: ${count} documents`;
            topicList.appendChild(listItem);
        }
    };

    const updateList = (listId, data) => {
        const list = document.getElementById(listId);
        list.innerHTML = "";
        for (const [user, count] of Object.entries(data)) {
            const listItem = document.createElement('li');
            listItem.textContent = `${user}: ${count}`;
            list.appendChild(listItem);
        }
    };

    fetchAnalytics();
});

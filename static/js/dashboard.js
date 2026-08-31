// ========================================
// Dashboard JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    initDashboard();
});

function initDashboard() {
    initSidebar();
    initCharts();
    initStatCards();
    initActivityFeed();
    initNotifications();
    initQuickActions();
    initDataTable();
}

// Sidebar Navigation
function initSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const navLinks = document.querySelectorAll('.sidebar-nav-link');
    const currentPath = window.location.pathname;
    
    // Set active link
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href)) {
            link.classList.add('active');
        }
    });
    
    // Sidebar toggle for mobile
    const menuToggle = document.querySelector('.menu-toggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            document.body.classList.toggle('sidebar-open');
        });
    }
    
    // Close sidebar on mobile when clicking a link
    if (window.innerWidth <= 1024) {
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                sidebar.classList.remove('open');
                document.body.classList.remove('sidebar-open');
            });
        });
    }
}

// Initialize Charts
function initCharts() {
    // Attendance Chart
    const attendanceCtx = document.getElementById('attendanceChart');
    if (attendanceCtx) {
        createAttendanceChart(attendanceCtx);
    }
    
    // Fee Collection Chart
    const feeCtx = document.getElementById('feeChart');
    if (feeCtx) {
        createFeeChart(feeCtx);
    }
    
    // Exam Results Chart
    const examCtx = document.getElementById('examChart');
    if (examCtx) {
        createExamChart(examCtx);
    }
}

function createAttendanceChart(ctx) {
    const data = JSON.parse(ctx.dataset.chartData || '[]');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Present',
                data: data.map(d => d.present),
                borderColor: '#10B981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.4
            }, {
                label: 'Absent',
                data: data.map(d => d.absent),
                borderColor: '#EF4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createFeeChart(ctx) {
    const data = JSON.parse(ctx.dataset.chartData || '[]');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Paid', 'Pending', 'Partial'],
            datasets: [{
                data: [
                    data.paid || 0,
                    data.pending || 0,
                    data.partial || 0
                ],
                backgroundColor: [
                    '#10B981',
                    '#EF4444',
                    '#F59E0B'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function createExamChart(ctx) {
    const data = JSON.parse(ctx.dataset.chartData || '[]');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.subject),
            datasets: [{
                label: 'Average Marks',
                data: data.map(d => d.average),
                backgroundColor: 'rgba(37, 99, 235, 0.8)',
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Stat Cards Animation
function initStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('stagger-item');
        
        // Counter animation
        const counter = card.querySelector('.counter-value');
        if (counter) {
            animateCounter(counter);
        }
    });
}

function animateCounter(element) {
    const target = parseInt(element.textContent.replace(/,/g, ''));
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// Activity Feed
function initActivityFeed() {
    const activityFeed = document.querySelector('.activity-feed');
    if (!activityFeed) return;
    
    const activities = activityFeed.querySelectorAll('.activity-item');
    activities.forEach((activity, index) => {
        activity.style.animationDelay = `${index * 0.1}s`;
        activity.classList.add('stagger-item');
    });
}

// Notifications
function initNotifications() {
    const notificationBtn = document.querySelector('.notification-btn');
    const notificationPanel = document.querySelector('.notifications-panel');
    
    if (notificationBtn && notificationPanel) {
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationPanel.classList.toggle('show');
        });
        
        document.addEventListener('click', function() {
            notificationPanel.classList.remove('show');
        });
    }
    
    // Mark as read
    const unreadNotifications = document.querySelectorAll('.notification-item.unread');
    unreadNotifications.forEach(notification => {
        notification.addEventListener('click', function() {
            this.classList.remove('unread');
        });
    });
}

// Quick Actions
function initQuickActions() {
    const quickActions = document.querySelectorAll('.quick-action');
    
    quickActions.forEach(action => {
        action.addEventListener('click', function() {
            const url = this.dataset.url;
            if (url) {
                window.location.href = url;
            }
        });
    });
}

// Data Table
function initDataTable() {
    const tables = document.querySelectorAll('.data-table');
    
    tables.forEach(table => {
        // Sort functionality
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(table, this.dataset.sort);
            });
        });
        
        // Row actions
        const actionButtons = table.querySelectorAll('.action-btn');
        actionButtons.forEach(btn => {
            btn.addEventListener('click', function(e) {
                const action = this.dataset.action;
                const id = this.dataset.id;
                
                if (action === 'delete') {
                    e.preventDefault();
                    confirmDelete(id, this);
                }
            });
        });
    });
}

function sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAscending = table.dataset.sortOrder !== 'asc';
    
    rows.sort((a, b) => {
        const aVal = a.querySelector(`td[data-column="${column}"]`).textContent;
        const bVal = b.querySelector(`td[data-column="${column}"]`).textContent;
        
        if (isAscending) {
            return aVal.localeCompare(bVal);
        } else {
            return bVal.localeCompare(aVal);
        }
    });
    
    rows.forEach(row => tbody.appendChild(row));
    table.dataset.sortOrder = isAscending ? 'asc' : 'desc';
}

function confirmDelete(id, button) {
    confirmDialog('Are you sure you want to delete this item?', function() {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = button.dataset.deleteUrl;
        
        const csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'csrf_token';
            input.value = csrfToken.content;
            form.appendChild(input);
        }
        
        document.body.appendChild(form);
        form.submit();
    });
}

// Filter Functionality
function initFilters() {
    const filterForms = document.querySelectorAll('.filter-form');
    
    filterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);
            
            // Update URL with filters
            window.location.href = `${window.location.pathname}?${params.toString()}`;
        });
    });
    
    // Clear filters
    const clearButtons = document.querySelectorAll('.filter-clear');
    clearButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            window.location.href = window.location.pathname;
        });
    });
}

// Export Functionality
function exportData(type, format) {
    const url = `/reports/export/${type}?format=${format}`;
    window.location.href = url;
}

// Print Function
function printPage() {
    window.print();
}

// Refresh Data
function refreshData() {
    location.reload();
}

// Export functions
window.exportData = exportData;
window.printPage = printPage;
window.refreshData = refreshData;

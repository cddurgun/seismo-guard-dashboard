// SEISMO-GUARD Dashboard JavaScript
// Real-time earthquake monitoring and visualization

// API Configuration - Auto-detect environment
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000/api'
    : (window.SEISMO_API_URL || `${window.location.origin}/api`);
const AUTO_REFRESH_INTERVAL = 300000; // 5 minutes

// Global state
let earthquakeMap = null;
let earthquakeMarkers = [];
let allEvents = [];
let charts = {};
let autoRefreshTimer = null;

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌍 SEISMO-GUARD Dashboard initializing...');
    initializeMap();
    initializeEventListeners();
    loadDashboardData();
    startAutoRefresh();
});

// Initialize Leaflet map
function initializeMap() {
    // Center on Turkey (Istanbul)
    earthquakeMap = L.map('earthquakeMap').setView([39.5, 35.0], 6);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18,
    }).addTo(earthquakeMap);

    // Add fault line overlay (simplified representation)
    addFaultLines();

    console.log('✓ Map initialized');
}

// Add major fault lines to map
function addFaultLines() {
    // North Anatolian Fault (simplified)
    const nafCoordinates = [
        [40.7, 27.0],
        [40.8, 28.5],
        [40.7, 30.0],
        [40.5, 32.0],
        [40.3, 34.0],
        [40.0, 36.0],
        [39.8, 38.0],
        [39.5, 40.0],
        [39.3, 42.0]
    ];

    L.polyline(nafCoordinates, {
        color: '#e94560',
        weight: 3,
        opacity: 0.7,
        dashArray: '10, 10'
    }).addTo(earthquakeMap).bindPopup('North Anatolian Fault');

    // East Anatolian Fault (simplified)
    const eafCoordinates = [
        [38.0, 36.5],
        [38.2, 37.5],
        [38.5, 38.5],
        [38.7, 39.5],
        [39.0, 40.5]
    ];

    L.polyline(eafCoordinates, {
        color: '#ff9800',
        weight: 3,
        opacity: 0.7,
        dashArray: '10, 10'
    }).addTo(earthquakeMap).bindPopup('East Anatolian Fault');
}

// Initialize event listeners
function initializeEventListeners() {
    // Refresh button
    document.getElementById('refreshBtn').addEventListener('click', function() {
        console.log('Manual refresh triggered');
        loadDashboardData();
    });

    // Region filter
    document.getElementById('regionFilter').addEventListener('change', function() {
        filterAndDisplayEvents();
    });

    // Magnitude filter
    document.getElementById('magnitudeFilter').addEventListener('change', function() {
        filterAndDisplayEvents();
    });
}

// Load all dashboard data
async function loadDashboardData() {
    try {
        console.log('📡 Fetching dashboard data...');

        // Show loading state
        updateLastUpdate('Updating...');

        // Fetch data in parallel
        const [eventsData, statsData, patternsData] = await Promise.all([
            fetchRecentEarthquakes(),
            fetchStatistics(),
            fetchPatterns()
        ]);

        // Update dashboard
        allEvents = eventsData.events || [];
        updateMetrics(statsData);
        displayEarthquakes(allEvents);
        displayPatterns(patternsData);
        createCharts(statsData);

        // Load risk assessments for key regions
        await loadRiskAssessments();

        // Update timestamp
        updateLastUpdate();

        console.log('✓ Dashboard data loaded successfully');
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showError('Failed to load dashboard data. Please check API connection.');
    }
}

// Fetch recent earthquakes
async function fetchRecentEarthquakes(hours = 168) {
    try {
        const response = await fetch(`${API_BASE_URL}/earthquakes/recent?hours=${hours}`);
        if (!response.ok) throw new Error('Failed to fetch earthquakes');
        return await response.json();
    } catch (error) {
        console.error('Error fetching earthquakes:', error);
        return { events: [], count: 0 };
    }
}

// Fetch statistics
async function fetchStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics/summary`);
        if (!response.ok) throw new Error('Failed to fetch statistics');
        return await response.json();
    } catch (error) {
        console.error('Error fetching statistics:', error);
        return null;
    }
}

// Fetch pattern analysis
async function fetchPatterns() {
    try {
        const response = await fetch(`${API_BASE_URL}/analysis/patterns`);
        if (!response.ok) throw new Error('Failed to fetch patterns');
        return await response.json();
    } catch (error) {
        console.error('Error fetching patterns:', error);
        return { temporal_patterns: [], spatial_clusters: [], anomalies: [] };
    }
}

// Update key metrics
function updateMetrics(stats) {
    if (!stats) return;

    document.getElementById('totalEvents').textContent = stats.total_events_24h || 0;
    document.getElementById('maxMagnitude').textContent =
        stats.max_magnitude_24h ? `M ${stats.max_magnitude_24h.toFixed(1)}` : 'N/A';
    document.getElementById('avgDepth').textContent =
        stats.avg_depth_km ? stats.avg_depth_km.toFixed(1) : 'N/A';
}

// Display earthquakes on map
function displayEarthquakes(events) {
    // Clear existing markers
    earthquakeMarkers.forEach(marker => marker.remove());
    earthquakeMarkers = [];

    if (!events || events.length === 0) {
        console.log('No events to display');
        return;
    }

    // Add markers for each event
    events.forEach(event => {
        const marker = createEarthquakeMarker(event);
        if (marker) {
            marker.addTo(earthquakeMap);
            earthquakeMarkers.push(marker);
        }
    });

    // Update events table
    updateEventsTable(events);

    console.log(`✓ Displayed ${events.length} earthquakes`);
}

// Create marker for earthquake event
function createEarthquakeMarker(event) {
    const mag = event.magnitude;

    // Determine marker color and size based on magnitude
    let color, radius;
    if (mag < 3.0) {
        color = '#4CAF50';
        radius = 5;
    } else if (mag < 4.0) {
        color = '#FFC107';
        radius = 8;
    } else if (mag < 5.0) {
        color = '#FF9800';
        radius = 12;
    } else {
        color = '#F44336';
        radius = 16;
    }

    // Create circle marker
    const marker = L.circleMarker([event.latitude, event.longitude], {
        radius: radius,
        fillColor: color,
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.7
    });

    // Create popup content
    const popupContent = `
        <div style="min-width: 200px;">
            <h3 style="margin: 0 0 10px 0; color: #1a1a2e;">
                M ${mag.toFixed(1)} Earthquake
            </h3>
            <p style="margin: 5px 0;"><strong>Location:</strong> ${event.location_name}</p>
            <p style="margin: 5px 0;"><strong>Region:</strong> ${event.region}</p>
            <p style="margin: 5px 0;"><strong>Depth:</strong> ${event.depth_km.toFixed(1)} km</p>
            <p style="margin: 5px 0;"><strong>Time:</strong> ${formatDateTime(event.timestamp)}</p>
            <p style="margin: 5px 0;"><strong>Source:</strong> ${event.source}</p>
            <p style="margin: 5px 0; font-size: 0.85em; color: #666;">
                ${event.latitude.toFixed(4)}°N, ${event.longitude.toFixed(4)}°E
            </p>
        </div>
    `;

    marker.bindPopup(popupContent);

    return marker;
}

// Filter and display events based on current filters
function filterAndDisplayEvents() {
    const regionFilter = document.getElementById('regionFilter').value;
    const magnitudeFilter = parseFloat(document.getElementById('magnitudeFilter').value);

    let filteredEvents = allEvents;

    // Apply region filter
    if (regionFilter !== 'all') {
        filteredEvents = filteredEvents.filter(e => e.region === regionFilter);
    }

    // Apply magnitude filter
    if (magnitudeFilter > 0) {
        filteredEvents = filteredEvents.filter(e => e.magnitude >= magnitudeFilter);
    }

    displayEarthquakes(filteredEvents);
}

// Update events table
function updateEventsTable(events) {
    const tbody = document.getElementById('eventsTableBody');
    tbody.innerHTML = '';

    if (!events || events.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="loading-text">No events to display</td></tr>';
        return;
    }

    // Show only significant events (M >= 2.5) in table, sorted by magnitude
    const significantEvents = events
        .filter(e => e.magnitude >= 2.5)
        .sort((a, b) => b.magnitude - a.magnitude)
        .slice(0, 10);

    significantEvents.forEach(event => {
        const row = document.createElement('tr');

        const magClass = getMagnitudeClass(event.magnitude);

        row.innerHTML = `
            <td>${formatTime(event.timestamp)}</td>
            <td><span class="magnitude-badge ${magClass}">M ${event.magnitude.toFixed(1)}</span></td>
            <td>${event.depth_km.toFixed(1)}</td>
            <td>${event.location_name}</td>
            <td>${event.region}</td>
        `;

        tbody.appendChild(row);
    });
}

// Get CSS class for magnitude badge
function getMagnitudeClass(mag) {
    if (mag < 3.0) return 'mag-low';
    if (mag < 4.0) return 'mag-medium';
    if (mag < 5.0) return 'mag-high';
    return 'mag-critical';
}

// Display detected patterns
function displayPatterns(patternsData) {
    const container = document.getElementById('patternsContent');
    container.innerHTML = '';

    const allPatterns = [
        ...(patternsData.temporal_patterns || []),
        ...(patternsData.spatial_clusters || []).map(c => ({
            type: 'spatial_cluster',
            description: c.description,
            ...c
        })),
        ...(patternsData.anomalies || [])
    ];

    if (allPatterns.length === 0) {
        container.innerHTML = '<p class="loading-text">No significant patterns detected</p>';
        return;
    }

    allPatterns.forEach(pattern => {
        const card = document.createElement('div');
        card.className = 'pattern-card';

        card.innerHTML = `
            <div class="pattern-type">${formatPatternType(pattern.type)}</div>
            <div class="pattern-description">${pattern.description}</div>
        `;

        container.appendChild(card);
    });
}

// Format pattern type for display
function formatPatternType(type) {
    const typeMap = {
        'rapid_sequence': '⚡ Rapid Sequence',
        'mainshock_sequence': '🎯 Mainshock Sequence',
        'spatial_cluster': '📍 Spatial Cluster',
        'shallow_depth': '⬇️ Shallow Depth Anomaly',
        'significant_magnitude': '⚠️ Significant Magnitude'
    };
    return typeMap[type] || type;
}

// Load risk assessments for key regions
async function loadRiskAssessments() {
    try {
        const response = await fetch(`${API_BASE_URL}/risk-assessment/Istanbul`);
        if (!response.ok) throw new Error('Failed to fetch risk assessment');

        const assessment = await response.json();
        displayRiskAssessment(assessment);

        // Update Istanbul risk level in metrics
        const riskElement = document.getElementById('istanbulRisk');
        riskElement.textContent = assessment.risk_level;
        riskElement.className = `metric-value risk-level ${assessment.risk_level.toLowerCase()}`;

    } catch (error) {
        console.error('Error loading risk assessment:', error);
    }
}

// Display risk assessment
function displayRiskAssessment(assessment) {
    const container = document.getElementById('riskAssessmentContent');

    container.innerHTML = `
        <div class="risk-info-item">
            <div class="risk-info-label">Region</div>
            <div class="risk-info-value">${assessment.region}</div>
        </div>
        <div class="risk-info-item">
            <div class="risk-info-label">Risk Level</div>
            <div class="risk-info-value risk-level ${assessment.risk_level.toLowerCase()}">
                ${assessment.risk_level}
            </div>
        </div>
        <div class="risk-info-item">
            <div class="risk-info-label">Confidence</div>
            <div class="risk-info-value">${assessment.confidence}%</div>
        </div>
        <div class="risk-info-item">
            <div class="risk-info-label">Trend</div>
            <div class="risk-info-value">${assessment.trend}</div>
        </div>
        <div class="risk-info-item">
            <div class="risk-info-label">7-Day M5+ Probability</div>
            <div class="risk-info-value">${(assessment.probability_m5_7days * 100).toFixed(1)}%</div>
        </div>
        <div class="risk-info-item">
            <div class="risk-info-label">30-Day M6+ Probability</div>
            <div class="risk-info-value">${(assessment.probability_m6_30days * 100).toFixed(1)}%</div>
        </div>
        <div class="risk-info-item">
            <div class="risk-info-label">Key Factors</div>
            <div style="font-size: 0.85rem; margin-top: 0.5rem;">
                ${assessment.contributing_factors.map(f => `• ${f}`).join('<br>')}
            </div>
        </div>
        <div class="risk-info-item">
            <div class="risk-info-label">Recommendations</div>
            <div style="font-size: 0.85rem; margin-top: 0.5rem;">
                ${assessment.recommendations.map(r => `• ${r}`).join('<br>')}
            </div>
        </div>
    `;
}

// Create charts
function createCharts(stats) {
    if (!stats) return;

    // Magnitude distribution chart
    createMagnitudeChart(stats.magnitude_distribution);

    // Depth distribution chart
    createDepthChart(stats.depth_distribution);

    // Timeline chart
    createTimelineChart();
}

// Create magnitude distribution chart
function createMagnitudeChart(magData) {
    const ctx = document.getElementById('magnitudeChart');

    if (charts.magnitude) {
        charts.magnitude.destroy();
    }

    charts.magnitude = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(magData || {}),
            datasets: [{
                label: 'Number of Events',
                data: Object.values(magData || {}),
                backgroundColor: [
                    'rgba(76, 175, 80, 0.7)',
                    'rgba(255, 193, 7, 0.7)',
                    'rgba(255, 152, 0, 0.7)',
                    'rgba(244, 67, 54, 0.7)',
                    'rgba(156, 39, 176, 0.7)'
                ],
                borderColor: [
                    'rgba(76, 175, 80, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(255, 152, 0, 1)',
                    'rgba(244, 67, 54, 1)',
                    'rgba(156, 39, 176, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#b8b8b8'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#b8b8b8'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

// Create depth distribution chart
function createDepthChart(depthData) {
    const ctx = document.getElementById('depthChart');

    if (charts.depth) {
        charts.depth.destroy();
    }

    charts.depth = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(depthData || {}),
            datasets: [{
                data: Object.values(depthData || {}),
                backgroundColor: [
                    'rgba(33, 150, 243, 0.7)',
                    'rgba(3, 169, 244, 0.7)',
                    'rgba(0, 188, 212, 0.7)',
                    'rgba(0, 150, 136, 0.7)'
                ],
                borderColor: '#1f1f3a',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#b8b8b8'
                    }
                }
            }
        }
    });
}

// Create timeline chart
function createTimelineChart() {
    const ctx = document.getElementById('timelineChart');

    if (charts.timeline) {
        charts.timeline.destroy();
    }

    // Group events by day
    const eventsByDay = {};
    allEvents.forEach(event => {
        const date = event.timestamp.split('T')[0];
        eventsByDay[date] = (eventsByDay[date] || 0) + 1;
    });

    const sortedDates = Object.keys(eventsByDay).sort();
    const counts = sortedDates.map(date => eventsByDay[date]);

    charts.timeline = new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedDates.map(d => formatDate(d)),
            datasets: [{
                label: 'Events per Day',
                data: counts,
                borderColor: 'rgba(233, 69, 96, 1)',
                backgroundColor: 'rgba(233, 69, 96, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: 'rgba(233, 69, 96, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#b8b8b8',
                        stepSize: 1
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#b8b8b8'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                }
            }
        }
    });
}

// Start auto-refresh
function startAutoRefresh() {
    autoRefreshTimer = setInterval(() => {
        console.log('🔄 Auto-refresh triggered');
        loadDashboardData();
    }, AUTO_REFRESH_INTERVAL);
}

// Update last update timestamp
function updateLastUpdate(text = null) {
    const element = document.getElementById('lastUpdate');
    if (text) {
        element.textContent = text;
    } else {
        const now = new Date();
        element.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
}

// Show error message
function showError(message) {
    console.error(message);
    // Could add toast notification here
}

// Utility: Format date time
function formatDateTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Utility: Format time only
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Utility: Format date
function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    });
}

console.log('✓ Dashboard JavaScript loaded');

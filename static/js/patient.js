document.addEventListener('DOMContentLoaded', () => {
    const adminToggle = document.querySelector('.flex.justify-between');
    const adminMenu = document.querySelector('.ml-4');

    adminToggle.addEventListener('click', () => {
        adminMenu.classList.toggle('hidden');
    });
});

const apiUrl = '/api/patient';

let patients = [];
let filteredPatients = [];
let currentPage = 1;
const pageSize = 50;

const fetchPatients = async () => {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        patients = data;
        filteredPatients = data;
        renderTable();
    } catch (error) {
        console.error("Error fetching patient data:", error);
    }
};

const renderTable = () => {
    const tableBody = document.getElementById("patient-table-body");
    tableBody.innerHTML = "";

    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pagePatients = filteredPatients.slice(start, end);

    pagePatients.forEach((patient) => {
        const row = `
<tr class="hover:bg-[#f9fafb] transition-colors duration-200">
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 capitalize">${patient.LAST}</td>
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 capitalize">${patient.FIRST}</td>
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">${patient.BIRTHDATE}</td>
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 capitalize">${patient.GENDER}</td>
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 capitalize">${patient.RACE}</td>
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 capitalize">${patient.ETHNICITY}</td>
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 capitalize">${patient.PASSPORT}</td>
<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 capitalize">${patient.CITY}</td>
<td class="px-6 py-4 whitespace-nowrap text-sm">
    <button
        class="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-full shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-300"
        onclick="showModal('${encodeURIComponent(JSON.stringify(patient))}')"
    >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Details
    </button>
</td>
</tr>
`;
        tableBody.innerHTML += row;
    });

    document.getElementById("pagination-info").textContent = `Page ${currentPage} of ${Math.ceil(filteredPatients.length / pageSize)}`;
};

const searchPatients = (searchTerm) => {
    filteredPatients = patients.filter((patient) =>
        Object.values(patient)
            .join(" ")
            .toLowerCase()
            .includes(searchTerm.toLowerCase())
    );
    currentPage = 1;
    renderTable();
};

let isLoading = false;

const showModal = async (encodedPatient) => {
    try {
        isLoading = true;
        document.getElementById("loading").classList.remove("hidden");

        const patient = JSON.parse(decodeURIComponent(encodedPatient));
        const observationsResponse = await fetch(`/api/observation/patient/${patient.Id}`);
        const medicationsResponse = await fetch(`/api/medication/patient/${patient.Id}`);
        const encountersResponse = await fetch(`/api/encounter/patient/${patient.Id}`);
        const immunizationsResponse = await fetch(`/api/immunization/patient/${patient.Id}`);
        const allergiesResponse = await fetch(`/api/allergies/patient/${patient.Id}`);
        const claimsResponse = await fetch(`/api/claim/patient/${patient.Id}`);
        const proceduresResponse = await fetch(`/api/procedure/patient/${patient.Id}`);

        const observations_data = await observationsResponse.json();
        const medications_data = await medicationsResponse.json();
        const encounters_data = await encountersResponse.json();
        const immunizations_data = await immunizationsResponse.json();
        const allergies_data = await allergiesResponse.json();
        const claims_data = await claimsResponse.json();
        const procedures_data = await proceduresResponse.json();

        document.getElementById("modal-content").innerHTML = `
<div>
    <div>
        <h1 class="my-1 text-center text-xl font-bold leading-8 text-[#111827]">${patient.FIRST} ${patient.LAST}</h1>
        <h3 class="font-lg text-semibold text-center leading-6 text-[#4b5563]">Patient</h3>

        <ul class="mt-3 divide-y divide-[#d1d5db] rounded bg-[#f3f4f6] px-3 py-2 text-[#4b5563] shadow-sm hover:text-[#374151] hover:shadow">
        <li class="flex items-center py-3 text-sm">
            <span>Age</span>
            <span class="ml-auto">${2024 - parseInt(patient.BIRTHDATE.slice(0, 5))}</span>
        </li>
        <li class="flex items-center py-3 text-sm">
            <span>Gender</span>
            <span class="ml-auto">${patient.GENDER}</span>
        </li>
        <li class="flex items-center py-3 text-sm">
            <span>Address</span>
            <span class="ml-auto">${patient.ADDRESS}</span>
        </li>
        <li class="flex items-center py-3 text-sm">
            <span>Birthplace</span>
            <span class="ml-auto">${patient.BIRTHPLACE}</span>
        </li>
        <li class="flex items-center py-3 text-sm">
            <span>Passport</span>
            <span class="ml-auto">${patient.PASSPORT}</span>
        </li>
        <li class="flex items-center py-3 text-sm">
            <span>SSN</span>
            <span class="ml-auto">${patient.SSN}</span>
        </li>
        <li class="flex items-center py-3 text-sm">
            <span>Healthcare Expenses</span>
            <span class="ml-auto">$${parseFloat(patient.HEALTHCARE_EXPENSES).toFixed(2)}</span>
        </li>
        <li class="flex items-center py-3 text-sm">
            <span>Healthcare Coverage</span>
            <span class="ml-auto">$${parseFloat(patient.HEALTHCARE_COVERAGE).toFixed(2)}</span>
        </li>
        </ul>
    </div>

    <div class="mt-4">
        <h1 class="text-center text-2xl font-bold py-2">Vitals over Time</h1>
        <canvas id="vitals-chart" class="w-100"></canvas>

        <h1 class="text-center text-2xl font-bold py-2 mt-4">Medication History Timeline</h1>
        <p class="text-center text-gray-200 pb-4 text-sm">Scroll inside to view the timeline. Hover over items for details.</p>
        <div id="timeline" class="scroll-wrapper"></div>

        <div id="encounter-list" class="p-6">
            <h2 class="text-2xl font-bold text-center text-gray-800 mb-4">Patient Encounter History</h2>
            <table class="w-full border-collapse bg-white shadow-md rounded-lg overflow-hidden">
                <thead class="bg-[#f3f4f6] border-b border-[#d1d5db]">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Procedure</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Start Date</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">End Date</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Healthcare Provider</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Claim Cost</th>
                    </tr>
                </thead>
                <tbody id="encounter-table-body" class="divide-y divide-[#e5e7eb]">
                    <!-- Encounter rows will be added here dynamically -->
                </tbody>
            </table>

            <div class="mt-4 flex justify-between items-center">
                <button id="prev-page" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50" disabled>Previous</button>
                <span id="page-number" class="text-lg font-semibold">Page 1</span>
                <button id="next-page" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Next</button>
            </div>
        </div>

        <h1 class="text-center text-2xl font-bold py-2 mt-4">Immunization History Timeline</h1>
        <p class="text-center text-gray-200 pb-4 text-sm">Scroll inside to view the timeline. Hover over items for details.</p>
        <div id="immunization-timeline" class="scroll-wrapper"></div>

        <h1 class="text-center text-2xl font-bold py-2 mt-4">Allergy Severity Chart</h1>
        <canvas id="allergyChart" width="800" height="400"></canvas>
        <p id="noDataMessage" style="display: none; text-align: center; color: red; font-size: 14px;">
            No allergies found for this patient.
        </p>

        <div id="claim-list" class="p-6">
            <h2 class="text-2xl font-bold text-center text-gray-800 mb-4">Claims Financial Transactions</h2>
            <table class="w-full border-collapse bg-white shadow-md rounded-lg overflow-hidden">
                <thead class="bg-[#f3f4f6] border-b border-[#d1d5db]">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Transaction Type</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Amount</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Payment Method</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Start Date</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">End Date</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Appointment</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Notes</th>
                    </tr>
                </thead>
                <tbody id="claim-table-body" class="divide-y divide-[#e5e7eb]">
                    <!-- Claim rows will be added here dynamically -->
                </tbody>
            </table>

            <div class="mt-4 flex justify-between items-center">
                <button id="prev-page-claim" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50" disabled>Previous</button>
                <span id="page-number-claim" class="text-lg font-semibold">Page 1</span>
                <button id="next-page-claim" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Next</button>
            </div>
        </div>

        <div id="procedure-list" class="p-6">
            <h2 class="text-2xl font-bold text-center text-gray-800 mb-4">Procedures Performed</h2>
            <table class="w-full border-collapse bg-white shadow-md rounded-lg overflow-hidden">
                <thead class="bg-[#f3f4f6] border-b border-[#d1d5db]">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Procedure</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Start Date</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">End Date</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Encounter</th>
                        <th class="px-6 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Reason</th>
                    </tr>
                </thead>
                <tbody id="procedure-table-body" class="divide-y divide-[#e5e7eb]">
                    <!-- Procedure rows will be added here dynamically -->
                </tbody>
            </table>

            <div class="mt-4 flex justify-between items-center">
                <button id="prev-page-procedure" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50" disabled>Previous</button>
                <span id="page-number-procedure" class="text-lg font-semibold">Page 1</span>
                <button id="next-page-procedure" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Next</button>
            </div>
        </div>

       <h2 class="text-2xl font-bold text-center text-gray-800 mb-4">Patient-Provider Network</h2>
        <div id="network-container" style="width: 100%; height: 500px; overflow: auto; border: 1px solid #ccc;">
            <svg id="network-map" style="width: 100%; height: 100%;"></svg>
        </div>
    </div>
</div>
`;
        const ctx_vitals = document.getElementById('vitals-chart').getContext('2d');

        // Grouping observations by type
        const groupedData = observations_data.data.observations.reduce((acc, obs) => {
            const date = new Date(obs.DATE).toISOString().split('T')[0]; // Get date part
            const { DESCRIPTION, VALUE } = obs;

            if (!acc[DESCRIPTION]) acc[DESCRIPTION] = { dates: [], values: [] };
            acc[DESCRIPTION].dates.push(date);
            acc[DESCRIPTION].values.push(parseFloat(VALUE));
            return acc;
        }, {});

        // Prepare datasets for Chart.js
        const datasets = Object.keys(groupedData).map((description, index) => {
            const colors = ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(75, 192, 192)"]; // Color set
            return {
                label: description,
                data: groupedData[description].values,
                borderColor: colors[index % colors.length],
                backgroundColor: colors[index % colors.length].replace('rgb', 'rgba').replace(')', ', 0.5)'),
                tension: 0.4,
            };
        });

        // Dates as labels (assuming all descriptions share the same dates)
        const labels_vitals = [...new Set(observations_data.data.observations.map(obs => new Date(obs.DATE).toISOString().split('T')[0]))];

        // Chart.js configuration
        const config = {
            type: 'line',
            data: {
                labels: labels_vitals,
                datasets: datasets
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Value'
                        },
                        beginAtZero: false
                    }
                }
            },
        };

        // Render the chart
        new Chart(ctx_vitals, config);

        // Medications Timeline
        const timelineData = medications_data.data.medications.map((medication, index) => ({
            id: index + 1,
            content: `${medication.DESCRIPTION} (${medication.DISPENSES} tablets)`,
            start: medication.START,
            end: medication.STOP || null,
            title: `Reason: ${medication.REASONDESCRIPTION}`, // Tooltip on hover
        }));

        // Create a timeline
        const container = document.getElementById('timeline');
        const items = new vis.DataSet(timelineData);

        const options = {
            start: "2010-01-01",
            end: "2020-01-01",
            editable: false,
            horizontalScroll: true, // Enables horizontal scrolling
            zoomKey: "ctrlKey", // Use CTRL + scroll to zoom
            zoomable: true, // Disable zooming to simplify UX
            margin: {
                item: 10,
                axis: 20
            },
            orientation: "top",
            min: "2000-01-01", // Prevent scrolling before 2000
            max: "2025-12-31", // Prevent scrolling after 2025
        };

        const timeline = new vis.Timeline(container, items, options);

        // Attach event for user hover to show more details in tooltip
        timeline.on('itemover', function (props) {
            console.log(`Hovered over: ${items.get(props.item).content}`);
        });


        // Encountersss
        const rowsPerPage = 5; // Number of rows per page
        let currentPage = 1;

        // Function to format date
        function formatDate(date) {
            const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
            return new Date(date).toLocaleDateString("en-US", options);
        }

        // Function to create table rows dynamically
        function renderEncounters() {
            const tableBody = document.getElementById("encounter-table-body");
            const startIndex = (currentPage - 1) * rowsPerPage;
            const endIndex = startIndex + rowsPerPage;
            const encountersToDisplay = encounters_data.data.encounters.slice(startIndex, endIndex);

            // Clear the current table content
            tableBody.innerHTML = '';

            encountersToDisplay.forEach(encounter => {
                const row = document.createElement("tr");
                row.className = "hover:bg-[#f9fafb] transition-colors duration-200";
                row.innerHTML = `
                <td class="px-6 py-4 text-sm text-gray-500">${encounter.DESCRIPTION}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${formatDate(encounter.START)}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${formatDate(encounter.STOP)}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${encounter.PROVIDER}</td>
                <td class="px-6 py-4 text-sm font-medium text-gray-900">$${parseFloat(encounter.TOTAL_CLAIM_COST).toFixed(2)}</td>
            `;
                tableBody.appendChild(row);
            });

            // Update page number display
            document.getElementById("page-number").textContent = `Page ${currentPage} of ${Math.ceil(encounters_data.data.encounters.length / rowsPerPage)}`;
            togglePaginationButtons();
        }

        // Toggle the state of the pagination buttons
        function togglePaginationButtons() {
            const prevButton = document.getElementById("prev-page");
            const nextButton = document.getElementById("next-page");

            prevButton.disabled = currentPage === 1;
            nextButton.disabled = currentPage * rowsPerPage >= encounters_data.data.encounters.length;
        }

        // Next page button click handler
        document.getElementById("next-page").addEventListener("click", () => {
            if (currentPage * rowsPerPage < encounters_data.data.encounters.length) {
                currentPage++;
                renderEncounters();
            }
        });

        // Previous page button click handler
        document.getElementById("prev-page").addEventListener("click", () => {
            if (currentPage > 1) {
                currentPage--;
                renderEncounters();
            }
        });

        // Initialize the page by rendering the first page
        renderEncounters();

        // Immunizations Timeline

        // Map immunization data to timeline format
        const timelineDataImmunization = immunizations_data.data.immunizations.map((immunization, index) => ({
            id: immunization.ID,
            content: `${immunization.DESCRIPTION}`,
            start: immunization.DATE,
            title: `Immunization ID: ${immunization.ID}`, // Tooltip on hover
        }));

        // Create a timeline data set
        const itemsImmunization = new vis.DataSet(timelineDataImmunization);

        // Timeline container
        const containerImmunization = document.getElementById('immunization-timeline');

        // Timeline options
        const optionsImmunization = {
            start: "1990-01-01", // Set a range for the timeline
            end: "2025-01-01", // Set the end range for the timeline
            editable: false,
            horizontalScroll: true, // Enables horizontal scrolling
            zoomKey: "ctrlKey", // Use CTRL + scroll to zoom
            zoomable: true, // Enable zooming
            margin: {
                item: 20,
                axis: 30
            },
            orientation: "top", // Position the axis on top
            min: "1980-01-01", // Prevent scrolling before 2015
            max: "2025-12-31", // Prevent scrolling after 2025
        };

        // Create and render the timeline
        const timelineImmunization = new vis.Timeline(containerImmunization, itemsImmunization, optionsImmunization);


        // Allergies Severity Chart

        // Convert severity levels to numerical values
        function severityToValue(severity) {
            switch (severity.trim().toUpperCase()) {
                case "MILD":
                    return 1;
                case "MODERATE":
                    return 2;
                case "SEVERE":
                    return 3;
                default:
                    return 0; // No severity mentioned
            }
        }

        // Check if there is any allergy data
        if (allergies_data.length === 0) {
            // Show "No allergies" message and hide the chart
            document.getElementById('allergyChart').style.display = 'none';
            document.getElementById('noDataMessage').style.display = 'block';
        } else {
            // Prepare data for Chart.js
            const labels = allergies_data.map(item => item.DESCRIPTION);
            function getSeverityFinal(severity1, severity2) {
                if (severity1.trim() !== "" && severity1.trim() !== "\r") {
                    return severity1.trim();
                }
                if (severity2.trim() !== "" && severity2.trim() !== "\r") {
                    return severity2.trim();
                }
                return "MILD";
            }
            const severity = allergies_data.map(item => severityToValue(getSeverityFinal(item.SEVERITY1 || "", item.SEVERITY2 || "")));

            // Chart.js Configuration
            const ctx = document.getElementById('allergyChart').getContext('2d');
            const allergyChart = new Chart(ctx, {
                type: 'bar', // Bar chart
                data: {
                    labels: labels, // Allergy descriptions
                    datasets: [
                        {
                            label: 'Severity',
                            data: severity,
                            backgroundColor: severity.map(value => {
                                if (value === 1) return 'rgba(54, 162, 235, 0.7)'; // MILD - Blue
                                if (value === 2) return 'rgba(255, 206, 86, 0.7)'; // MODERATE - Yellow
                                if (value === 3) return 'rgba(255, 99, 132, 0.7)'; // SEVERE - Red
                                return 'rgba(201, 203, 207, 0.7)'; // NONE - Gray
                            }),
                            borderColor: 'rgba(0, 0, 0, 0.1)',
                            borderWidth: 1,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const value = context.raw;
                                    const severityLevel = value === 1 ? 'MILD' : value === 2 ? 'MODERATE' : value === 3 ? 'SEVERE' : 'NONE';
                                    return `${context.dataset.label}: ${severityLevel}`;
                                },
                            },
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Allergies',
                            },
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Severity Level',
                            },
                            ticks: {
                                stepSize: 1, // Display integers
                                callback: function (value) {
                                    // Convert numerical values back to severity names
                                    if (value === 1) return 'MILD';
                                    if (value === 2) return 'MODERATE';
                                    if (value === 3) return 'SEVERE';
                                    return 'NONE';
                                },
                            },
                        },
                    },
                },
            });
        }

        // Claim Transactions
        const rowsPerPageClaims = 5; // Number of rows per page
        let currentPageClaims = 1;

        // Function to create table rows dynamically
        function renderClaims() {
            const tableBody = document.getElementById("claim-table-body");
            const startIndex = (currentPageClaims - 1) * rowsPerPageClaims;
            const endIndex = startIndex + rowsPerPageClaims;
            const claimsToDisplay = claims_data.data.claims.slice(startIndex, endIndex);

            // Clear the current table content
            tableBody.innerHTML = '';

            claimsToDisplay.forEach(claim => {
                const row = document.createElement("tr");
                row.className = "hover:bg-[#f9fafb] transition-colors duration-200";
                row.innerHTML = `
                <td class="px-6 py-4 text-sm text-gray-500">${claim.TYPE ?? "-"}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${claim.AMOUNT ? "$" + parseFloat(claim.AMOUNT).toFixed(2) : "-"}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${claim.METHOD || "-"}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${formatDate(claim.FROMDATE)}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${formatDate(claim.TODATE)}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${claim.APPOINTMENTID ?? "-"}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${claim.NOTES ?? "-"}</td>
            `;
                tableBody.appendChild(row);
            });

            // Update page number display
            document.getElementById("page-number-claim").textContent = `Page ${currentPageClaims} of ${Math.ceil(claims_data.data.claims.length / rowsPerPageClaims)}`;
            togglePaginationButtonsForClaims();
        }

        // Toggle the state of the pagination buttons
        function togglePaginationButtonsForClaims() {
            const prevButton = document.getElementById("prev-page-claim");
            const nextButton = document.getElementById("next-page-claim");

            prevButton.disabled = currentPageClaims === 1;
            nextButton.disabled = currentPageClaims * rowsPerPageClaims >= claims_data.data.claims.length;
        }

        // Next page button click handler
        document.getElementById("next-page-claim").addEventListener("click", () => {
            if (currentPageClaims * rowsPerPageClaims < claims_data.data.claims.length) {
                currentPageClaims++;
                renderClaims();
            }
        });

        // Previous page button click handler
        document.getElementById("prev-page-claim").addEventListener("click", () => {
            if (currentPageClaims > 1) {
                currentPageClaims--;
                renderClaims();
            }
        });

        // Initialize the page by rendering the first page
        renderClaims();

        // Procedures Performed Table
        const rowsPerPageProcedure = 5; // Number of rows per page
        let currentPageProcedure = 1;

        // Function to create table rows dynamically
        function renderProcedures() {
            const tableBody = document.getElementById("procedure-table-body");
            const startIndex = (currentPageProcedure - 1) * rowsPerPageProcedure;
            const endIndex = startIndex + rowsPerPageProcedure;
            const proceduresToDisplay = procedures_data.data.procedures.slice(startIndex, endIndex);

            // Clear the current table content
            tableBody.innerHTML = '';

            proceduresToDisplay.forEach(procedure => {
                const row = document.createElement("tr");
                row.className = "hover:bg-[#f9fafb] transition-colors duration-200";
                row.innerHTML = `
                <td class="px-6 py-4 text-sm text-gray-500">${procedure.DESCRIPTION}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${formatDate(procedure.START)}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${formatDate(procedure.STOP)}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${procedure.ENCOUNTER || "-"}</td>
                <td class="px-6 py-4 text-sm text-gray-500">${procedure.REASONDESCRIPTION || "-"}</td>
            `;
                tableBody.appendChild(row);
            });

            // Update page number display
            document.getElementById("page-number-procedure").textContent = `Page ${currentPageProcedure} of ${Math.ceil(procedures_data.data.procedures.length / rowsPerPageProcedure)}`;
            togglePaginationButtonsForProcedures();
        }

        // Toggle the state of the pagination buttons
        function togglePaginationButtonsForProcedures() {
            const prevButton = document.getElementById("prev-page-procedure");
            const nextButton = document.getElementById("next-page-procedure");

            prevButton.disabled = currentPageProcedure === 1;
            nextButton.disabled = currentPageProcedure * rowsPerPageProcedure >= procedures_data.data.procedures.length;
        }

        // Next page button click handler
        document.getElementById("next-page-procedure").addEventListener("click", () => {
            if (currentPageProcedure * rowsPerPageProcedure < procedures_data.data.procedures.length) {
                currentPageProcedure++;
                renderProcedures();
            }
        });

        // Previous page button click handler
        document.getElementById("prev-page-procedure").addEventListener("click", () => {
            if (currentPageProcedure > 1) {
                currentPageProcedure--;
                renderProcedures();
            }
        });

        // Initialize the page by rendering the first page
        renderProcedures();

        // Network Map
        // Prepare nodes and links
        const nodes = [];
        const links = [];
        const nodeSet = new Set();

        encounters_data.data.encounters.forEach(encounter => {
            const patientId = encounter.PATIENT;
            const providerId = encounter.PROVIDER;

            if (!nodeSet.has(patientId)) {
                nodes.push({ id: patientId, type: "Patient", label: `Patient (${patient.FIRST} ${patient.LAST})` });
                nodeSet.add(patientId);
            }

            if (!nodeSet.has(providerId)) {
                nodes.push({ id: providerId, type: "Provider", label: `Provider (${providerId})` });
                nodeSet.add(providerId);
            }

            links.push({
                source: providerId,
                target: patientId,
                type: "Encounter"
            });
        });

        const svg = d3.select("#network-map"),
            width = 1000,
            height = 600;

        // Create a container for zoom and pan
        const container2 = svg.append("g");

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(150))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = container2.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("class", "link");

        const node = container2.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(nodes)
            .enter().append("g")

        node.append("circle")
            .attr("r", 10)
            .attr("fill", d => d.type === "Patient" ? "lightblue" : "orange");

        node.append("text")
            .attr("x", 15)
            .attr("y", 3)
            .text(d => d.label);

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("transform", d => `translate(${d.x},${d.y})`);
        });

        // Add zoom and pan
        const zoom = d3.zoom()
            .scaleExtent([0.5, 3]) // Zoom levels
            .on("zoom", event => {
                container2.attr("transform", event.transform);
            });

        svg.call(zoom);
        document.getElementById("modal").classList.remove("hidden");
    } catch (error) {
        console.error(error);
    } finally {
        isLoading = false;
        document.getElementById("loading").classList.add("hidden");
    }
}

const closeModal = () => {
    document.getElementById("modal").classList.add("hidden");
};

document.getElementById("search").addEventListener("input", (e) => searchPatients(e.target.value));
document.getElementById("prev").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
    }
});
document.getElementById("next").addEventListener("click", () => {
    if (currentPage < Math.ceil(filteredPatients.length / pageSize)) {
        currentPage++;
        renderTable();
    }
});
document.getElementById("close-modal").addEventListener("click", closeModal);

const modalContainer = document.getElementById('modal');
modalContainer.addEventListener('click', (event) => {
    if (event.target === modalContainer) {
        closeModal();
    }
});

// Fetch and render the patient data on load
fetchPatients();

let sortDirection = {}; // Track the sort direction for each column

const sortTable = (column) => {
    // Toggle sort direction for the column
    if (!sortDirection[column]) {
        sortDirection[column] = 'asc';
    } else {
        sortDirection[column] = sortDirection[column] === 'asc' ? 'desc' : 'asc';
    }

    // Sort filteredPatients based on the column and direction
    filteredPatients.sort((a, b) => {
        const aValue = a[column];
        const bValue = b[column];

        if (aValue < bValue) {
            return sortDirection[column] === 'asc' ? -1 : 1;
        }
        if (aValue > bValue) {
            return sortDirection[column] === 'asc' ? 1 : -1;
        }
        return 0;
    });

    // Reset to the first page and re-render the table
    currentPage = 1;
    renderTable();
};

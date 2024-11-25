const BASE_URL = "/api";

let isLoading = false;

async function getData() {
    const maleCount = { key: "male", value: 0 };
    const femaleCount = { key: "female", value: 0 };
    const ageCounts = {
        "2-16": 0,
        "17-30": 0,
        "31-45": 0,
        "46-65": 0,
        "65+": 0,
    };
    const raceCounts = {
        White: 0,
        Black: 0,
        Asian: 0,
        Other: 0,
    };

    try {
        isLoading = true;
        document.getElementById("loading").classList.remove("hidden");

        const patientData = await axios.get(`${BASE_URL}/patient`);
        const patients = patientData.data;

        const cityCounts = {};
        patients.forEach((entry) => {
            const cityName = entry.CITY;
            cityCounts[cityName] = (cityCounts[cityName] || 0) + 1;
        });

        const cities = Object.entries(cityCounts).map(([name, count]) => ({
            name: name,
            count,
        }));
        cities.sort((a, b) => b.count - a.count);
        const citiesData = cities.filter((city) => city.name != "Unknown")

        patients.forEach((entry) => {
            const gender = entry.GENDER ?? "unspecified";
            if (gender === "M") {
                maleCount.value++;
            } else if (gender === "F") {
                femaleCount.value++;
            }

            const birthYear = entry.BIRTHDATE ? parseInt(entry.BIRTHDATE.slice(0, 4)) : undefined;
            const race = entry.RACE;

            if (birthYear) {
                const age = 2024 - birthYear;
                if (age <= 16) ageCounts["2-16"]++;
                else if (age <= 30) ageCounts["17-30"]++;
                else if (age <= 45) ageCounts["31-45"]++;
                else if (age <= 65) ageCounts["46-65"]++;
                else ageCounts["65+"]++;
            }

            if (race === "white") raceCounts["White"]++;
            else if (race === "black") raceCounts["Black"]++;
            else if (race === "asian") raceCounts["Asian"]++;
            else raceCounts["Other"]++;
        });

        const practitionerData = await axios.get(`${BASE_URL}/provider`);
        const practitionerCount = practitionerData.data.data.providers.length;

        const maxAgeRange = Object.entries(ageCounts).reduce((max, current) => {
            return current[1] > max[1] ? current : max;
        }, ["", 0])[0];

        const FILTER_MEDICATIONS_NAMES = {
            "NDA020503 200 ACTUAT Albuterol 0.09 MG/ACTUAT Metered Dose Inhaler":
                "Albuterol",
            "120 ACTUAT Fluticasone propionate 0.044 MG/ACTUAT Metered Dose Inhaler":
                "Fluticasone",
            "24 HR Metformin hydrochloride 500 MG Extended Release Oral Tablet":
                "Metformin",
            "insulin human  isophane 70 UNT/ML / Regular Insulin  Human 30 UNT/ML Injectable Suspension [Humulin]":
                "isophane",
            "1 ML medroxyPROGESTERone acetate 150 MG/ML Injection": "Medroxyprogesterone",
        };
        const response = await axios.get(`${BASE_URL}/medication`);
        const medicationEntries = response.data.data.medications;

        const medicationCounts = {};
        medicationEntries.forEach((entry) => {
            const medicationName = FILTER_MEDICATIONS_NAMES[entry.DESCRIPTION]
                ? FILTER_MEDICATIONS_NAMES[entry.DESCRIPTION]
                : entry.DESCRIPTION.split(" ")[0].charAt(0).toUpperCase() +
                entry.DESCRIPTION.split(" ")[0].slice(1).toLowerCase() ||
                "Unknown";
            medicationCounts[medicationName] =
                (medicationCounts[medicationName] || 0) + 1;
        });

        const medicationUsage = Object.entries(medicationCounts).map(
            ([name, count]) => ({
                name: name,
                count,
            })
        );

        medicationUsage.sort((a, b) => b.count - a.count);
        popularMedication = medicationUsage[0].name;
        const medicationsData = medicationUsage.filter((medication) => medication.name != "Unknown")

        const claimResponse = await axios.get(`${BASE_URL}/claim`);
        const claimEntries = claimResponse.data.data.claims;

        const transformedData = claimEntries.map((entry) => ({
            id: entry.ID,
            created: entry.FROMDATE,
            total: entry.AMOUNT || entry.PAYMENTS,
        }));

        const costData = transformedData
            .filter((data) => data.total > 0 && data.created)
            .sort((a, b) => a.created.localeCompare(b.created))
            .slice(70)

        const encounterResponse = await axios.get(`${BASE_URL}/encounter`);
        const encounterData = encounterResponse.data.data.encounters.map((entry) => ({
            id: entry.Id,
            class: entry?.ENCOUNTERCLASS || "-",
        }));

        const conditionResponse = await axios.get(`${BASE_URL}/condition`);
        const conditionData = conditionResponse.data.data.conditions;

        const observationsResponse = await axios.get(`${BASE_URL}/observation?type=survey`);
        let { observations: data } = observationsResponse.data.data;

        data
            .filter((data) => data.TYPE === "numeric" && data.DATE)
            .forEach((d) => {
                d.DATE = new Date(d.DATE);
                d.VALUE = +d.VALUE;
            });

        data = data.filter(
            (d) => d.DATE instanceof Date && !isNaN(d.DATE.getTime())
        );

        data.sort((a, b) => a.DATE.getTime() - b.DATE.getTime());

        const groupedData = d3.group(data, (d) => d3.timeFormat("%Y")(d.DATE));

        const averageData = Array.from(groupedData, ([key, values]) => ({
            YEAR: key,
            value: d3['mean'](values, (d) => d.VALUE),
        }));

        const observationsData = averageData
            .filter((d) => !isNaN(Number(d.YEAR)) && !isNaN(d.value))
            .map((data) => {
                return {
                    date: new Date(data.YEAR),
                    value: data.value <= 10 ? data.value : 9.5,
                };
            });

        updateUI({
            maleCount: (maleCount.value / patients.length) * 100,
            femaleCount: (femaleCount.value / patients.length) * 100,
            totalPatients: patients.length,
            popularMedication: popularMedication,
            medicationsData: medicationsData,
            citiesData: citiesData,
            costData: costData,
            encounterData: encounterData,
            conditionData: conditionData,
            observationsData: observationsData,
            maxAgeRange,
            practitionerCount,
            ageData: Object.entries(ageCounts),
            raceData: Object.entries(raceCounts),
        });

    } catch (error) {
        console.error(error);
    } finally {
        isLoading = false;
        document.getElementById("loading").classList.add("hidden");
    }
}

function updateUI({
    maleCount,
    femaleCount,
    totalPatients,
    popularMedication,
    maxAgeRange,
    practitionerCount,
    ageData,
    raceData,
    medicationsData,
    costData,
    encounterData,
    conditionData,
    observationsData,
    citiesData
}) {
    // Update Card Data Stats
    const cardContainer = document.getElementById("content");
    cardContainer.innerHTML = `

<div class="grid-cols-4 mb-8 grid gap-7">
    <div
        class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="text-primary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="lucide lucide-users">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
        </div>

        <div class="mt-4 flex items-end justify-between">
            <div>
                <h4 class="text-title-md font-bold text-black dark:text-white">
                    ${totalPatients}
                </h4>
                <span class="text-sm font-medium">Total Patients</span>
            </div>
        </div>
    </div>

    <div
        class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="text-primary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-pill"><path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/></svg>
        </div>

        <div class="mt-4 flex items-end justify-between">
            <div>
                <h4 class="text-title-md font-bold text-black dark:text-white">
                    ${popularMedication || "Paracetamol"}
                </h4>
                <span class="text-sm font-medium">Most Prescribed Medication</span>
            </div>
        </div>
    </div>

    <div
        class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="text-primary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user-round"><circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/></svg>
        </div>

        <div class="mt-4 flex items-end justify-between">
            <div>
                <h4 class="text-title-md font-bold text-black dark:text-white">
                    ${maxAgeRange}
                </h4>
                <span class="text-sm font-medium">Majority Age Group</span>
            </div>
        </div>
    </div>

    <div
        class="rounded-sm border border-stroke bg-white px-7.5 py-6 shadow-default dark:border-strokedark dark:bg-boxdark">
        <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
            <svg class="text-primary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-stethoscope"><path d="M11 2v2"/><path d="M5 2v2"/><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/></svg>
        </div>

        <div class="mt-4 flex items-end justify-between">
            <div>
                <h4 class="text-title-md font-bold text-black dark:text-white">
                    ${practitionerCount}
                </h4>
                <span class="text-sm font-medium">Total Practitioners</span>
            </div>
        </div>
    </div>
</div>
`;

    // Update Charts
    const chartsContainer = document.getElementById("charts");
    chartsContainer.innerHTML = `
<div class="rounded-sm border border-stroke bg-white pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark px-7.5 col-span-3">
      <div class="mb-3 justify-between gap-4 flex">
        <div>
          <h5 class="text-xl font-semibold text-black dark:text-white">
            Gender Distribution (Patients)
          </h5>
        </div>
      </div>

      <div class="mb-2 mt-8">
        <div id="chart-one" class="mx-auto flex justify-center">
          
        </div>
      </div>

      <div class="mx-8 mt-12 flex items-center justify-center gap-y-3">
        <div class="w-full px-8">
          <div class="flex w-full items-center">
            <span class="mr-2 block h-3 w-6 max-w-3 rounded-full bg-[#FFC0CB]"></span>
            <p class="flex w-full justify-between text-sm font-medium text-black dark:text-white">
              <span> Female </span>
            </p>
          </div>
        </div>

        <div class="w-full px-8">
          <div class="flex w-full items-center">
            <span class="mr-2 block h-3 w-6 max-w-3 rounded-full bg-primary"></span>
            <p class="flex w-full justify-between text-sm font-medium text-black dark:text-white">
              <span> Male </span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="rounded-sm border border-stroke bg-white pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark px-7.5 col-span-9">
      <div class="mb-3 justify-between gap-4 flex">
        <div>
          <h5 class="text-xl font-semibold text-black dark:text-white">
            Top 10 Commonly Prescribed Medications
          </h5>
        </div>
      </div>

      <div class="overflow-x-auto">
        <div id="chart-two" class="-ml-5">

        </div>
      </div>
    </div>

    <div class="rounded-sm border border-stroke bg-white p-7.5 shadow-default dark:border-strokedark dark:bg-boxdark col-span-6">
      <div class="mb-4 justify-between gap-4 flex">
        <div>
          <h4 class="text-xl font-semibold text-black dark:text-white">
            Race Distribution (Patients)
          </h4>
        </div>
      </div>

      <div class="overflow-x-auto">
        <div id="chart-three" class="ml-8 mr-6">
        </div>
      </div>
    </div>

    <div class="rounded-sm border border-stroke bg-white pb-5 pt-7.5 p-7.5 shadow-default dark:border-strokedark dark:bg-boxdark col-span-6">
      <div class="mb-3 justify-between gap-4 flex">
        <div>
          <h4 class="text-xl font-semibold text-black dark:text-white">
            City Distribution (Patients)
          </h4>
        </div>
      </div>

      <div class="overflow-x-auto">
        <div id="chart-four" class="-ml-5">
        </div>
      </div>
    </div>

    <div class="rounded-sm border border-stroke bg-white p-7.5 shadow-default dark:border-strokedark dark:bg-boxdark col-span-7">
      <div class="mb-4 justify-between gap-4 flex">
          <h4 class="text-xl font-semibold text-black dark:text-white">
            Patient Satisfaction Score
          </h4>
        </div>

      <div class="overflow-x-auto">
        <div id="chart-five" class="-ml-5">
        </div>
      </div>
    </div>

    <div class="rounded-sm border border-stroke bg-white p-7.5 shadow-default dark:border-strokedark dark:bg-boxdark col-span-5">
      <div class="mb-4 justify-between gap-4 sm:flex">
        <div>
          <h4 class="text-xl font-semibold text-black dark:text-white">
            Age Distribution (Patients)
          </h4>
        </div>
      </div>

      <div class="overflow-x-auto">
        <div id="chart-six" class="-ml-5">
        </div>
      </div>
    </div>

    <div class="rounded-sm border border-stroke bg-white pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark px-7.5 col-span-9">
      <div class="mb-3 justify-between gap-4 flex">
        <div>
          <h5 class="text-xl font-semibold text-black dark:text-white">
            Cost Trends Over Time (in USD)
          </h5>
        </div>
      </div>
      <div class="overflow-x-auto">
        <div class="ml-5">
            <div class="flex items-center gap-16">
                <div class="w-full" id="chart-seven">
                </div>
            </div>
        </div>
      </div>
    </div>

    <div class="rounded-sm border border-stroke bg-white pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark px-7.5 col-span-3">
      <div class="mb-3 justify-between gap-4 sm:flex">
        <div>
          <h5 class="text-xl font-semibold text-black dark:text-white">
            Types of Visits
          </h5>
        </div>
      </div>

      <div class="mb-2 mt-8">
        <div id="chart-eight" class="mx-auto flex justify-center">
        </div>
      </div>

      <div class="mx-8 mt-12 flex justify-center gap-x-12 gap-y-3">
        <div class="flex items-center">
          <span class="mr-2 block h-3 w-6 max-w-3 rounded-full bg-[#f28e2c]"></span>
          <p class="text-sm font-medium text-black dark:text-white">
            Outpatient
          </p>
        </div>

        <div class="flex items-center">
          <span class="mr-2 block h-3 w-6 max-w-3 rounded-full bg-[#4e79a7]"></span>
          <p class="text-sm font-medium text-black dark:text-white">
            Inpatient
          </p>
        </div>
      </div>
    </div>

    <div class="items-center justify-center rounded-sm border border-stroke bg-white pb-5 pt-7.5 shadow-default dark:border-strokedark dark:bg-boxdark px-7.5 col-span-12">
      <div class="mb-3 justify-between gap-4 flex">
        <div>
          <h5 class="text-xl font-semibold text-black dark:text-white">
            Top 10 Prevalent Conditions
          </h5>
        </div>
      </div>
      <div class="mt-8 flex w-full items-center justify-center">
        <div
          id="chart-nine"
          class="ml-5 flex w-full items-center justify-center"
        >
        </div>
      </div>
    </div>
    `;

    renderDonutChart('chart-one', [{ value: maleCount }, { value: femaleCount }]);
    renderBarChart('chart-two', medicationsData);
    renderRaceBarChart('chart-three', raceData);
    renderCityBarChart('chart-four', citiesData);
    renderObservationsLineChart('chart-five', observationsData);
    renderAgeBarChart('chart-six', ageData);
    renderCostAreaChart('chart-seven', costData);
    renderEncounterPieChart('chart-eight', encounterData);
    renderConditionTreeMapChart('chart-nine', conditionData);
}

function renderDonutChart(containerId, data) {
    const svg = d3.select(`#${containerId}`)
        .append('svg')
        .attr('width', 200)
        .attr('height', 200);

    const radius = 100;
    const color = d3.scaleOrdinal(['#FFC0CB', '#3C50E0']);
    const pie = d3.pie().value(d => d.value);

    const arc = d3.arc()
        .innerRadius(60)
        .outerRadius(100);

    // Tooltip creation
    const tooltip = d3.select(`#${containerId}`)
        .append('div')
        .style('position', 'absolute')
        .style('background', '#fff')
        .style('padding', '8px')
        .style('border-radius', '4px')
        .style('box-shadow', '0px 2px 4px rgba(0, 0, 0, 0.2)')
        .style('pointer-events', 'none')
        .style('opacity', 0);

    const g = svg.selectAll('.arc')
        .data(pie(data))
        .enter().append('g')
        .attr('class', 'arc')
        .attr('transform', 'translate(100,100)')
        .on('mouseover', handleMouseOver)
        .on('mousemove', handleMouseMove)
        .on('mouseout', handleMouseLeave);

    g.append('path')
        .attr('d', arc)
        .style('fill', (d, i) => color(i))
        .style('opacity', 0.8)
        .style('transition', 'opacity 0.3s ease, font-weight 0.3s ease');

    function handleMouseOver(event, d) {
        d3.select(this)
            .select('path')
            .style('opacity', 1);

        tooltip
            .style('opacity', 1)
            .html(`
                ${d.data.value.toFixed(2)}%
            `);
    }

    function handleMouseMove(event) {
        tooltip
            .style('left', `${event.pageX + 10}px`)
            .style('top', `${event.pageY + 10}px`);
    }

    function handleMouseLeave(event, d) {
        d3.select(this)
            .select('path')
            .style('opacity', 0.8);

        tooltip.style('opacity', 0);
    }
}


function renderBarChart(containerId, data) {
    const container = document.getElementById(containerId);
    const totalMedicines = data.reduce((sum, item) => sum + item.count, 0);
    const topMedicines = data.slice(0, 10).map(item => ({
        name: item.name,
        count: ((item.count / totalMedicines) * 100).toFixed(2)
    }));

    const width = 1100;
    const height = 300;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const maxValue = Math.max(...topMedicines.map(d => parseFloat(d.count)));

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", width);
    svg.setAttribute("height", height);
    container.appendChild(svg);

    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("transform", `translate(${margin.left},${margin.top})`);
    svg.appendChild(g);

    const xScale = d3.scaleBand()
        .domain(topMedicines.map(d => d.name))
        .range([0, innerWidth])
        .padding(0.6);

    const yScale = d3.scaleLinear()
        .domain([0, maxValue])
        .range([innerHeight, 0]);

    // Bars
    topMedicines.forEach((d, index) => {
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", xScale(d.name));
        rect.setAttribute("y", yScale(d.count));
        rect.setAttribute("width", xScale.bandwidth());
        rect.setAttribute("height", innerHeight - yScale(d.count));
        rect.setAttribute("fill", "#0FADCF");
        rect.setAttribute("class", "cursor-pointer");
        rect.style.opacity = 0.8;

        rect.addEventListener("mouseover", () => {
            rect.style.opacity = 1;
            tooltip.style.visibility = "visible";
            tooltip.textContent = `${d.count}%`;
            tooltip.setAttribute("x", xScale(d.name) + xScale.bandwidth() / 2);
            tooltip.setAttribute("y", yScale(d.count) - 5);
        });

        rect.addEventListener("mouseleave", () => {
            rect.style.opacity = 0.8;
            tooltip.style.visibility = "hidden";
        });

        g.appendChild(rect);
    });

    // Tooltip
    const tooltip = document.createElementNS("http://www.w3.org/2000/svg", "text");
    tooltip.setAttribute("font-size", "12");
    tooltip.setAttribute("font-weight", "500");
    tooltip.setAttribute("text-anchor", "middle");
    tooltip.setAttribute("fill", "#000");
    tooltip.style.visibility = "hidden";
    g.appendChild(tooltip);

    // Axes
    const xAxis = d3.axisBottom(xScale);
    const xAxisGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    xAxisGroup.setAttribute("transform", `translate(0,${innerHeight})`);
    d3.select(xAxisGroup).call(xAxis);
    g.appendChild(xAxisGroup);

    const yAxis = d3.axisLeft(yScale);
    const yAxisGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    d3.select(yAxisGroup).call(yAxis);
    g.appendChild(yAxisGroup);
}

function renderRaceBarChart(containerId, rawData) {
    const totalData = rawData.reduce((sum, [, value]) => sum + value, 0);
    const data = rawData.map(([label, value]) => [
        label,
        +((value / totalData) * 100).toFixed(2),
    ]);
    const maxValue = Math.max(...data.map(([, value]) => value));
    const width = 580;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const yScale = d3
        .scaleBand()
        .domain(data.map(([label]) => label))
        .range([0, innerHeight])
        .padding(0.4);

    const xScale = d3.scaleLinear().domain([0, maxValue]).range([0, innerWidth]);

    const colorScale = d3
        .scaleSequential(d3.interpolateBlues)
        .domain([0, maxValue]);

    const svg = d3
        .select(`#${containerId}`)
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const chartGroup = svg
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const tooltip = d3
        .select(`#${containerId}`)
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("background", "#fff")
        .style("color", "#000")
        .style("border", "1px solid #ccc")
        .style("padding", "5px")
        .style("display", "none");

    chartGroup
        .selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", 0)
        .attr("y", ([label]) => yScale(label))
        .attr("width", ([, value]) => xScale(value))
        .attr("height", yScale.bandwidth())
        .attr("fill", ([, value]) => colorScale(value))
        .on("mouseover", function (event, [label, value]) {
            tooltip
                .style("display", "block")
                .html(`<strong>${label}:</strong> ${value.toFixed(2)}%`)
                .style("left", `${event.pageX + 10}px`)
                .style("top", `${event.pageY + 10}px`);
        })
        .on("mousemove", function (event) {
            tooltip
                .style("left", `${event.pageX + 10}px`)
                .style("top", `${event.pageY + 10}px`);
        })
        .on("mouseout", function () {
            tooltip.style("display", "none");
        });

    chartGroup.append("g").call(d3.axisLeft(yScale));
}

function renderCityBarChart(containerId, data) {
    const container = document.getElementById(containerId);
    container.innerHTML = ''; // Clear previous content

    const filteredCities = data
    const totalCities = filteredCities.reduce((a, b) => a + b.count, 0);

    const topCities = filteredCities.slice(0, 15).map(data => ({
        name: data.name,
        count: ((data.count / totalCities) * 100).toFixed(2),
    }));

    // Chart dimensions
    const width = 1000;
    const height = 400;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const maxValue = Math.max(...topCities.map(d => d.count));

    // Scales
    const xScale = d3
        .scaleBand()
        .domain(topCities.map(d => d.name))
        .range([0, innerWidth])
        .padding(0.2);

    const yScale = d3.scaleLinear().domain([0, maxValue]).range([innerHeight, 0]);

    const colorScale = d3
        .scaleSequential(d3.interpolateGreens)
        .domain([0, maxValue]);

    // Create SVG
    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const chartGroup = svg
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Bars
    chartGroup
        .selectAll('.bar')
        .data(topCities)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', d => xScale(d.name))
        .attr('y', d => yScale(d.count))
        .attr('width', xScale.bandwidth())
        .attr('height', d => innerHeight - yScale(d.count))
        .attr('fill', d => colorScale(d.count))
        .style('opacity', 0.8)
        .on('mouseover', handleMouseOver)
        .on('mouseout', handleMouseLeave);

    // Axes
    chartGroup
        .append('g')
        .attr('transform', `translate(0,${innerHeight})`)
        .call(d3.axisBottom(xScale))
        .selectAll('text')
        .style('text-anchor', 'center');

    chartGroup.append('g').call(d3.axisLeft(yScale));

    // Tooltip
    const tooltip = d3.select(container)
        .append('div')
        .attr('class', 'tooltip')
        .style('position', 'absolute')
        .style('background', '#fff')
        .style("color", "#000")
        .style('padding', '5px')
        .style('border', '1px solid #ccc')
        .style('border-radius', '5px')
        .style('pointer-events', 'none')
        .style('display', 'none');

    function handleMouseOver(event, d) {
        tooltip
            .style('display', 'block')
            .style('left', `${event.pageX + 10}px`)
            .style('top', `${event.pageY - 20}px`)
            .html(`<strong>${d.name}</strong>: ${d.count}%`);
    }

    function handleMouseLeave() {
        tooltip.style('display', 'none');
    }
}

function renderAgeBarChart(containerId, data) {
    // Calculate total data for percentage calculation
    const totalData = data.reduce((a, b) => a + b[1], 0);
    const filteredData = data.map(d => [
        d[0],
        +((d[1] / totalData) * 100).toFixed(2)
    ]);
    data = filteredData;

    // Calculate maximum value for scaling the bars
    const maxValue = Math.max(...data.map(([_, value]) => value));

    // Chart dimensions
    const width = 560;
    const height = 425;
    const margin = { top: 20, right: 30, bottom: 30, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Scales
    const xScale = d3
        .scaleBand()
        .domain(data.map(([label]) => label))
        .range([0, innerWidth])
        .padding(0.5);

    const yScale = d3.scaleLinear().domain([0, maxValue]).range([innerHeight, 0]);

    // Select the container and append SVG
    const svg = d3
        .select(`#${containerId}`)
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const g = svg
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Create bars
    g.selectAll(".bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", ([label]) => xScale(label))
        .attr("y", ([, value]) => yScale(value))
        .attr("width", xScale.bandwidth())
        .attr("height", ([, value]) => innerHeight - yScale(value))
        .attr("fill", "#f28e2c")
        .style("cursor", "pointer")
        .style("opacity", 0.9)
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseLeave);

    // Add text labels
    g.selectAll(".label")
        .data(data)
        .enter()
        .append("text")
        .attr("x", ([label]) => xScale(label) + xScale.bandwidth() / 2)
        .attr("y", ([, value]) => yScale(value) - 5)
        .attr("text-anchor", "middle")
        .attr("font-size", 12)
        .attr("font-weight", 500)
        .text(([label, value]) => `${value.toFixed(2)}%`)
        .style("visibility", "hidden")
        .attr("class", "tooltip");

    // X-axis
    g.append("g")
        .attr("transform", `translate(0,${innerHeight})`)
        .call(d3.axisBottom(xScale));

    // Y-axis
    g.append("g").call(d3.axisLeft(yScale));

    // Tooltip handlers
    function handleMouseOver(event, [label, value]) {
        d3.select(this).style("opacity", 1);
        g.selectAll(".tooltip")
            .filter(d => d[0] === label)
            .style("visibility", "visible")
            .text(`${value.toFixed(2)}%`);
    }

    function handleMouseLeave() {
        d3.select(this).style("opacity", 0.9);
        g.selectAll(".tooltip").style("visibility", "hidden");
    }
}

function renderCostAreaChart(containerId, data) {
    // Parse dates and values
    const parsedData = data.map(d => ({
        date: new Date(d.created),
        value: d?.total ?? 0,
    }));

    // Aggregate data by month
    const aggregatedData = d3.rollup(
        parsedData,
        v => d3.mean(v, d => d.value),
        d => d3.timeMonth(d.date)
    );

    const aggregatedDataArray = Array.from(aggregatedData, ([key, value]) => ({
        date: new Date(key),
        value,
    }));

    // Set up dimensions
    const parentWidth = 1500;
    const parentHeight = 390;
    const margin = { top: 20, right: 120, bottom: 30, left: 40 };
    const width = parentWidth - margin.left - margin.right;
    const height = parentHeight - margin.top - margin.bottom;

    // Remove previous chart if exists
    d3.select(`#${containerId}`).selectAll("*").remove();

    // Create SVG element
    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Set up scales
    const xScale = d3.scaleTime()
        .domain(d3.extent(aggregatedDataArray, d => d.date))
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(aggregatedDataArray, d => d.value) || 0])
        .range([height, 0]);

    // Create area generator
    const area = d3.area()
        .x(d => xScale(d.date))
        .y0(height)
        .y1(d => yScale(d.value));

    // Add area to SVG
    svg.append("path")
        .datum(aggregatedDataArray)
        .attr("fill", "rgba(26,143,251, 0.3)")
        .attr("stroke", "#1A8FFB")
        .attr("stroke-width", 2)
        .attr("d", area);

    // Add axes
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale));

    svg.append("g")
        .call(d3.axisLeft(yScale));

    // Tooltip setup
    const tooltip = d3.select(`#${containerId}`)
        .append("div")
        .attr("class", "tooltip")
        .style("display", "none")
        .style("position", "absolute")
        .style("background", "#fff")
        .style("color", "#000")
        .style("border", "1px solid #ccc")
        .style("padding", "5px")
        .style("border-radius", "3px")
        .style("pointer-events", "none");

    // Add interactive dots
    svg.selectAll(".dot")
        .data(aggregatedDataArray)
        .enter()
        .append("circle")
        .attr("class", "dot")
        .attr("cx", d => xScale(d.date))
        .attr("cy", d => yScale(d.value))
        .attr("r", 4)
        .attr("fill", "#1A8FFB")
        .on("mouseover", (event, d) => {
            tooltip.style("display", "block")
                .html(`Value: ${d.value.toFixed(2)}<br>Date: ${d3.timeFormat("%Y-%m")(d.date)}`)
                .style("left", `${event.pageX + 10}px`)
                .style("top", `${event.pageY - 20}px`);
        })
        .on("mouseout", () => tooltip.style("display", "none"));
}

function renderEncounterPieChart(containerId, encounters) {
    // Categories for grouping encounters
    const categories = {
        Inpatient: ["IMP", "inpatient", "inpatient encounter", "wellness"],
        Outpatient: ["AMB", "ambulatory", "Ambulatorio", "outpatient"]
    };

    // Group encounters by category
    const groupedEncounters = Object.keys(categories).reduce((acc, category) => {
        acc[category] = encounters.filter(encounter =>
            categories[category].includes(encounter.class)
        ).length;
        return acc;
    }, {});

    const totalEncounters = Object.values(groupedEncounters).reduce(
        (sum, value) => sum + value,
        0
    );

    const data = Object.entries(groupedEncounters).map(([category, count]) => ({
        category: category,
        count: (count / totalEncounters) * 100
    }));

    // Remove any existing SVG in the container
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    // Dimensions for the pie chart
    const width = 230;
    const height = 320;
    const radius = Math.min(width, height) / 2;

    // Color scale
    const color = d3.scaleOrdinal(d3.schemeTableau10);

    // Create SVG container
    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    // Create pie and arc generators
    const arc = d3.arc().innerRadius(0).outerRadius(radius);
    const pie = d3.pie().value(d => d.count).sort(null);

    // Tooltip
    const tooltip = d3
        .select(`#${containerId}`)
        .append("div")
        .style("position", "absolute")
        .style("background", "#fff")
        .style("padding", "8px")
        .style("border-radius", "4px")
        .style("box-shadow", "0px 2px 4px rgba(0, 0, 0, 0.2)")
        .style("pointer-events", "none")
        .style("opacity", 0);

    // Bind data and create arcs
    const arcs = svg.selectAll("arc").data(pie(data)).enter().append("g");

    arcs
        .append("path")
        .attr("d", arc)
        .attr("fill", (d, i) => color(i))
        .attr("stroke", "white")
        .style("stroke-width", "2px")
        .on("mouseover", function (event, d) {
            d3.select(this).attr("opacity", 1).attr("cursor", "pointer");

            tooltip
                .style("opacity", 1)
                .style("left", `${event.pageX + 10}px`)
                .style("top", `${event.pageY + 10}px`)
                .html(`
          <strong>${d.data.category}</strong><br>
          ${d.data.count.toFixed(2)}%
        `);
        })
        .on("mousemove", function (event) {
            tooltip
                .style("left", `${event.pageX + 10}px`)
                .style("top", `${event.pageY + 10}px`);
        })
        .on("mouseout", function () {
            d3.select(this).attr("opacity", 0.8);
            tooltip.style("opacity", 0);
        });
}

function renderConditionTreeMapChart(containerId, data) {
    const container = document.getElementById(containerId);

    // Clear existing content
    container.innerHTML = "";

    // Process data
    const conditionsCount = {};
    data.forEach(item => {
        const condition = item?.DESCRIPTION;
        if (condition) {
            conditionsCount[condition] = (conditionsCount[condition] || 0) + 1;
        }
    });

    const conditionsArray = Object.keys(conditionsCount).map(key => ({
        condition: key.replace(/\s*\([^)]*\)\s*/g, ""),
        count: conditionsCount[key],
    }));

    conditionsArray.sort((a, b) => b.count - a.count);

    const top10Conditions = conditionsArray
        .filter(data => data.condition !== "undefined")
        .slice(0, 10);

    // Dimensions
    const width = 1500; // Full width of the container
    const height = 600; // Fixed height

    // Treemap setup
    const treemap = d3.treemap().size([width, height]).padding(2).round(true);

    const root = d3
        .hierarchy({ children: top10Conditions })
        .sum(d => d.count);
    treemap(root);

    const colorScale = d3
        .scaleSequential(d3.interpolateBlues)
        .domain([0, d3.max(top10Conditions.map(d => d.count))]);

    // Create the SVG
    const svg = d3
        .select(container)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .style("font-family", "Arial, sans-serif")
        .style("overflow-x", "auto") // Allows horizontal scroll
        .style("overflow-y", "hidden");

    // Add cells
    const cell = svg
        .selectAll("g")
        .data(root.leaves())
        .enter()
        .append("g")
        .attr("transform", d => `translate(${d.x0},${d.y0})`)
        .style("cursor", "pointer");

    // Add rectangles with hover color change effect
    cell
        .append("rect")
        .attr("width", d => d.x1 - d.x0)
        .attr("height", d => d.y1 - d.y0)
        .attr("fill", d => colorScale(d.data.count))
        .attr("rx", 5) // Rounded corners
        .attr("ry", 5)
        .style("transition", "fill 0.2s ease") // Smooth transition for fill color
        .on("mouseover", function () {
            d3.select(this).style("fill", function (d) {
                return d3.rgb(colorScale(d.data.count)).darker(0.2); // Darken the color on hover
            });
        })
        .on("mouseout", function () {
            d3.select(this).style("fill", function (d) {
                return colorScale(d.data.count); // Reset the original color on mouseout
            });
        });

    // Add labels with text truncation
    cell
        .append("text")
        .attr("x", 5)
        .attr("y", 20)
        .attr("font-size", "14px")
        .attr("fill", "#fff")
        .style("text-shadow", "0px 2px 4px rgba(0,0,0,0.6)")
        .style("white-space", "nowrap") // Ensures no line breaks
        .style("overflow", "hidden") // Hidden overflow for long text
        .style("text-overflow", "ellipsis") // Adds ellipsis for long text
        .text(d => d.data.condition)

    // Tooltip setup
    const tooltip = d3
        .select(container)
        .append("div")
        .style("position", "absolute")
        .style("background", "rgba(255, 255, 255, 0.9)")
        .style("padding", "10px")
        .style("border-radius", "6px")
        .style("box-shadow", "0px 4px 6px rgba(0, 0, 0, 0.2)")
        .style("pointer-events", "none")
        .style("opacity", 0)
        .style("font-size", "14px");

    cell
        .on("mouseover", function (event, d) {
            d3.select(this).select("rect").style("stroke", "#333").style("stroke-width", "2px");
            tooltip
                .style("opacity", 1)
                .html(`
                    <strong>${d.data.condition}</strong><br>
                    Count: ${d.data.count}
                `);
        })
        .on("mousemove", function (event) {
            tooltip
                .style("left", `${event.pageX + 10}px`)
                .style("top", `${event.pageY + 10}px`);
        })
        .on("mouseout", function () {
            d3.select(this).select("rect").style("stroke", "none");
            tooltip.style("opacity", 0);
        });
}

function renderObservationsLineChart(containerId, data) {
    const container = document.getElementById(containerId);
    if (!container || !data) return;

    const svg = d3.select(container).append('svg')
        .attr('width', 850)
        .attr('height', 425);

    const margin = { top: 20, right: 0, bottom: 10, left: 80 };
    const width = svg.attr('width') - margin.left - margin.right;
    const height = svg.attr('height') - margin.top - margin.bottom;

    const x = d3.scaleTime()
        .domain(d3.extent(data, (d) => d.date))
        .range([margin.left, width - margin.right]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, (d) => d.value)]).nice()
        .range([height - margin.bottom, margin.top]);

    const xAxis = (g) => g.attr('transform', `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(width / 80).tickSizeOuter(0));

    const yAxis = (g) => g.attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y))
        .call((g) => g.select('.tick:last-of-type text')
            .clone()
            .attr('x', 3)
            .attr('text-anchor', 'start')
            .attr('font-weight', 'bold'));

    const line = d3.line()
        .x((d) => x(d.date))
        .y((d) => y(d.value));

    svg.selectAll('*').remove();  // Remove any existing content

    svg.append('g').call(xAxis);
    svg.append('g').call(yAxis);

    svg.append('path')
        .datum(data)
        .attr('fill', 'none')
        .attr('stroke', '#6577F3')
        .attr('stroke-width', 2)
        .attr('d', line);

    // Tooltip setup
    const tooltip = d3
        .select(`#${containerId}`)
        .append("div")
        .style("position", "absolute")
        .style("background", "#fff")
        .style("padding", "8px")
        .style("border-radius", "4px")
        .style("box-shadow", "0px 2px 4px rgba(0, 0, 0, 0.2)")
        .style("pointer-events", "none")
        .style("opacity", 0);

    // Dots
    svg.selectAll('.dot')
        .data(data)
        .enter().append('circle')
        .attr('class', 'dot')
        .attr('cx', (d) => x(d.date))
        .attr('cy', (d) => y(d.value))
        .attr('r', 3)
        .style('fill', '#6577F3')
        .style('cursor', 'pointer')
        .on('mouseover', function (event, d) {
            const [xPos, yPos] = d3.pointer(event);
            tooltip
                .style("opacity", 1)
                .style("left", `${event.pageX + 10}px`)
                .style("top", `${event.pageY + 10}px`)
                .html(`
                    <strong>${d.date.toLocaleDateString()}</strong><br>
                    Score: ${d.value.toFixed(2)}/10
                `);
        })
        .on('mousemove', function (event) {
            tooltip
                .style("left", `${event.pageX + 10}px`)
                .style("top", `${event.pageY + 10}px`);
        })
        .on('mouseout', function () {
            tooltip.style("opacity", 0);
        });
}



getData();

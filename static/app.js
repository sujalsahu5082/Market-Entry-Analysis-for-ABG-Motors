// JavaScript Logic - ABG Motors Dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Current Active Model sub-tab state
    let activeModelName = 'Logistic Regression';
    let apiData = {
        stats: null,
        models: null,
        indianPredictions: null
    };

    // Chart references for destruction on update
    let charts = {};

    // Elements
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    const viewTitle = document.getElementById('view-title');
    const viewSubtitle = document.getElementById('view-subtitle');

    // Sidebar navigation switching
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            navItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');

            const tabId = this.getAttribute('data-tab');
            tabContents.forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById(tabId).classList.add('active');

            // Update title and subtitle
            switch(tabId) {
                case 'overview':
                    viewTitle.innerText = "Dashboard Overview";
                    viewSubtitle.innerText = "Strategic analysis for entering the Indian automobile market";
                    break;
                case 'eda':
                    viewTitle.innerText = "Customer Demographics (EDA)";
                    viewSubtitle.innerText = "Exploratory analysis of customer characteristics in Japan and India";
                    break;
                case 'models':
                    viewTitle.innerText = "Model Evaluation & Tuning";
                    viewSubtitle.innerText = "Comparative analysis of Logistic Regression, Decision Trees, and Random Forests";
                    break;
                case 'predictor':
                    viewTitle.innerText = "Interactive Purchase Predictor";
                    viewSubtitle.innerText = "Test individual customer profiles using our trained classifiers";
                    break;
                case 'recommendations':
                    viewTitle.innerText = "Strategic Business Verdict";
                    viewSubtitle.innerText = "ABG Motors market entry framework and recommendations";
                    break;
            }
        });
    });

    // -------------------------------------------------------------
    // Fetch and Load Data
    // -------------------------------------------------------------
    async function loadDashboardData() {
        try {
            const statsRes = await fetch('/api/stats');
            apiData.stats = await statsRes.json();

            const modelsRes = await fetch('/api/models');
            apiData.models = await modelsRes.json();

            const indRes = await fetch('/api/predict_indian_market');
            apiData.indianPredictions = await indRes.json();

            // Populate initial dashboard values
            populateOverviewKPIs();
            renderOverviewChart();
            renderEDACharts();
            renderROCChart();
            updateModelTabUI();
            
            // Set up predictor initial state
            triggerPrediction();
        } catch (err) {
            console.error("Error loading dashboard APIs:", err);
        }
    }

    // -------------------------------------------------------------
    // Tab: Overview Page
    // -------------------------------------------------------------
    function populateOverviewKPIs() {
        if (!apiData.indianPredictions) return;

        // Use Random Forest as the recommended primary forecast
        const rfPred = apiData.indianPredictions['Random Forest'];
        const lrPred = apiData.indianPredictions['Logistic Regression'];
        const dtPred = apiData.indianPredictions['Decision Tree'];

        const numBuyers = rfPred.potential_buyers;
        const targetSales = 12000;
        const diffPercent = ((numBuyers - targetSales) / targetSales * 100).toFixed(1);

        document.getElementById('buyer-metric').innerText = numBuyers.toLocaleString();
        document.getElementById('verdict-buyers').innerText = numBuyers.toLocaleString();
        
        const marginEl = document.getElementById('margin-metric');
        if (numBuyers >= targetSales) {
            marginEl.innerText = `+${diffPercent}%`;
            marginEl.className = "metric-value text-green";
        } else {
            marginEl.innerText = `${diffPercent}%`;
            marginEl.className = "metric-value text-red";
        }
    }

    function renderOverviewChart() {
        if (!apiData.indianPredictions) return;

        const ctx = document.getElementById('overviewChart').getContext('2d');
        
        const rfBuyers = apiData.indianPredictions['Random Forest'].potential_buyers;
        const lrBuyers = apiData.indianPredictions['Logistic Regression'].potential_buyers;
        const dtBuyers = apiData.indianPredictions['Decision Tree'].potential_buyers;
        
        if (charts.overview) charts.overview.destroy();

        charts.overview = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Target', 'Logistic Regression', 'Decision Tree', 'Random Forest'],
                datasets: [{
                    label: 'Annual Sales Volume / Potential Buyers',
                    data: [12000, lrBuyers, dtBuyers, rfBuyers],
                    backgroundColor: [
                        'rgba(245, 158, 11, 0.4)',  // Target: Orange
                        'rgba(59, 130, 246, 0.5)',  // LR: Blue
                        'rgba(16, 185, 129, 0.5)',  // DT: Green
                        'rgba(139, 92, 246, 0.6)'   // RF: Purple
                    ],
                    borderColor: [
                        '#f59e0b',
                        '#3b82f6',
                        '#10b981',
                        '#8b5cf6'
                    ],
                    borderWidth: 2,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8' }
                    }
                }
            }
        });
    }

    // -------------------------------------------------------------
    // Tab: Customer Demographics (EDA)
    // -------------------------------------------------------------
    function renderEDACharts() {
        if (!apiData.stats) return;

        const stats = apiData.stats;

        // 1. Age Purchase Rate
        const ctxAgePurchase = document.getElementById('agePurchaseChart').getContext('2d');
        if (charts.agePurchase) charts.agePurchase.destroy();
        charts.agePurchase = new Chart(ctxAgePurchase, {
            type: 'bar',
            data: {
                labels: Object.keys(stats.jp_age_purchase),
                datasets: [{
                    label: 'Purchase Likelihood (%)',
                    data: Object.values(stats.jp_age_purchase).map(v => (v * 100).toFixed(1)),
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: '#3b82f6',
                    borderWidth: 1.5,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8', callback: value => value + '%' }
                    },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // 2. Income Purchase Rate
        const ctxIncomePurchase = document.getElementById('incomePurchaseChart').getContext('2d');
        if (charts.incomePurchase) charts.incomePurchase.destroy();
        charts.incomePurchase = new Chart(ctxIncomePurchase, {
            type: 'line',
            data: {
                labels: Object.keys(stats.jp_income_purchase),
                datasets: [{
                    label: 'Purchase Rate (%)',
                    data: Object.values(stats.jp_income_purchase).map(v => (v * 100).toFixed(1)),
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    borderColor: '#10b981',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8', callback: value => value + '%' }
                    },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // 3. Age Distribution (Japan vs India)
        const ctxAgeDist = document.getElementById('ageDistributionChart').getContext('2d');
        if (charts.ageDist) charts.ageDist.destroy();
        charts.ageDist = new Chart(ctxAgeDist, {
            type: 'bar',
            data: {
                labels: Object.keys(stats.jp_age_dist),
                datasets: [
                    {
                        label: 'Japan (Training Pool)',
                        data: Object.values(stats.jp_age_dist),
                        backgroundColor: 'rgba(139, 92, 246, 0.4)',
                        borderColor: '#8b5cf6',
                        borderWidth: 1
                    },
                    {
                        label: 'India (Target Pool)',
                        data: Object.values(stats.in_age_dist),
                        backgroundColor: 'rgba(245, 158, 11, 0.4)',
                        borderColor: '#f59e0b',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#f1f5f9' } }
                },
                scales: {
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });
    }

    // -------------------------------------------------------------
    // Tab: Model Evaluation
    // -------------------------------------------------------------
    const modelSubTabs = document.querySelectorAll('.sub-tab');
    modelSubTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            modelSubTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            const selected = this.getAttribute('data-model-tab');
            if (selected === 'logistic') activeModelName = 'Logistic Regression';
            else if (selected === 'dt') activeModelName = 'Decision Tree';
            else if (selected === 'rf') activeModelName = 'Random Forest';
            
            updateModelTabUI();
        });
    });

    function updateModelTabUI() {
        if (!apiData.models) return;

        // Default to showing 4-feature models metrics (as they include the full feature scope)
        const metrics = apiData.models.models_4_features[activeModelName];
        
        // Gauge KPI numbers
        document.getElementById('model-accuracy').innerText = (metrics.accuracy * 100).toFixed(1) + "%";
        document.getElementById('model-precision').innerText = (metrics.precision * 100).toFixed(1) + "%";
        document.getElementById('model-recall').innerText = (metrics.recall * 100).toFixed(1) + "%";
        document.getElementById('model-f1').innerText = (metrics.f1 * 100).toFixed(1) + "%";

        // Confusion Matrix
        const cm = metrics.confusion_matrix;
        document.getElementById('cm-tn').innerText = cm[0][0].toLocaleString();
        document.getElementById('cm-fp').innerText = cm[0][1].toLocaleString();
        document.getElementById('cm-fn').innerText = cm[1][0].toLocaleString();
        document.getElementById('cm-tp').innerText = cm[1][1].toLocaleString();

        // Model explanation paragraphs
        const notesEl = document.getElementById('model-notes');
        if (activeModelName === 'Logistic Regression') {
            notesEl.innerHTML = "<strong>Logistic Regression</strong> serves as our interpretable linear baseline. Hyperparameter grid-search optimization converges on a regularization strength C=0.01 with standard lbfgs solver. This model is exceptionally clean to export but has a slightly higher rate of false-positives compared to tree ensemble architectures.";
        } else if (activeModelName === 'Decision Tree') {
            notesEl.innerHTML = "Our <strong>Decision Tree Classifier</strong> is constrained to max_depth=10, min_samples_leaf=4, and min_samples_split=10 to eliminate overfitting risks. It achieves an accuracy of ~69%, isolating decision paths. Income levels and current car ownership age act as the root partitioning features.";
        } else if (activeModelName === 'Random Forest') {
            notesEl.innerHTML = "The <strong>Random Forest Ensemble</strong> combines 100 estimators to yield high generalization accuracy. Out-of-bag verification shows the lowest variance of all tested models, making it the most reliable baseline for calculating our market entry yield counts. Income is weighted as the highest informative feature.";
        }

        // Feature Importance Chart
        renderFeatureImportance(metrics.feature_importances);
    }

    function renderFeatureImportance(importances) {
        const ctx = document.getElementById('featureImportanceChart').getContext('2d');
        if (charts.featureImportance) charts.featureImportance.destroy();

        // Map column display names
        const labelsMap = {
            'CURR_AGE': 'Current Age',
            'GENDER': 'Gender',
            'ANN_INCOME': 'Annual Income',
            'AGE_CAR': 'Age of Car',
            'GENDER_Female': 'Gender (Female)'
        };
        const labels = Object.keys(importances).map(l => labelsMap[l] || l);
        const data = Object.values(importances).map(v => (v * 100).toFixed(1));

        charts.featureImportance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Relative Feature Contribution (%)',
                    data: data,
                    backgroundColor: 'rgba(139, 92, 246, 0.5)',
                    borderColor: '#8b5cf6',
                    borderWidth: 1.5,
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#94a3b8', callback: value => value + '%' }
                    },
                    y: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });
    }

    function renderROCChart() {
        if (!apiData.models) return;

        const ctx = document.getElementById('rocChart').getContext('2d');
        if (charts.roc) charts.roc.destroy();

        const lrRoc = apiData.models.models_4_features['Logistic Regression'].roc;
        const dtRoc = apiData.models.models_4_features['Decision Tree'].roc;
        const rfRoc = apiData.models.models_4_features['Random Forest'].roc;

        charts.roc = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: `Logistic Regression (AUC = ${lrRoc.auc.toFixed(2)})`,
                        data: lrRoc.fpr.map((fpr, i) => ({ x: fpr, y: lrRoc.tpr[i] })),
                        borderColor: '#3b82f6',
                        borderWidth: 2,
                        pointRadius: 0,
                        fill: false
                    },
                    {
                        label: `Decision Tree (AUC = ${dtRoc.auc.toFixed(2)})`,
                        data: dtRoc.fpr.map((fpr, i) => ({ x: fpr, y: dtRoc.tpr[i] })),
                        borderColor: '#10b981',
                        borderWidth: 2,
                        pointRadius: 0,
                        fill: false
                    },
                    {
                        label: `Random Forest (AUC = ${rfRoc.auc.toFixed(2)})`,
                        data: rfRoc.fpr.map((fpr, i) => ({ x: fpr, y: rfRoc.tpr[i] })),
                        borderColor: '#8b5cf6',
                        borderWidth: 2,
                        pointRadius: 0,
                        fill: false
                    },
                    {
                        label: 'Random Guess',
                        data: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
                        borderColor: 'rgba(255, 255, 255, 0.15)',
                        borderWidth: 1,
                        borderDash: [5, 5],
                        pointRadius: 0,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { labels: { color: '#94a3b8', font: { size: 10 } } }
                },
                scales: {
                    x: {
                        type: 'linear',
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        title: { display: true, text: 'False Positive Rate', color: '#94a3b8' },
                        ticks: { color: '#94a3b8' },
                        min: 0,
                        max: 1
                    },
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        title: { display: true, text: 'True Positive Rate', color: '#94a3b8' },
                        ticks: { color: '#94a3b8' },
                        min: 0,
                        max: 1
                    }
                }
            }
        });
    }

    // -------------------------------------------------------------
    // Tab: Interactive Predictor
    // -------------------------------------------------------------
    const ageInput = document.getElementById('age-input');
    const ageVal = document.getElementById('age-val-display');
    const incomeInput = document.getElementById('income-input');
    const incomeVal = document.getElementById('income-val-display');
    const carAgeInput = document.getElementById('car-age-input');
    const carAgeVal = document.getElementById('car-age-val-display');
    const includeCarAge = document.getElementById('include-car-age');
    const carAgeGroup = document.getElementById('car-age-group');
    const form = document.getElementById('prediction-form');

    // Update range displays
    ageInput.addEventListener('input', () => { ageVal.innerText = ageInput.value; });
    incomeInput.addEventListener('input', () => { 
        incomeVal.innerText = "₹ " + parseInt(incomeInput.value).toLocaleString('en-IN'); 
    });
    carAgeInput.addEventListener('input', () => { carAgeVal.innerText = carAgeInput.value; });

    // Show/hide car age slider
    includeCarAge.addEventListener('change', function() {
        if (this.checked) {
            carAgeGroup.style.display = 'flex';
        } else {
            carAgeGroup.style.display = 'none';
        }
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        triggerPrediction();
    });

    async function triggerPrediction() {
        const age = parseFloat(ageInput.value);
        const gender = parseInt(document.querySelector('input[name="gender"]:checked').value);
        const income = parseFloat(incomeInput.value);
        const hasCarAge = includeCarAge.checked;
        const carAge = hasCarAge ? parseFloat(carAgeInput.value) : null;

        try {
            const res = await fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    age: age,
                    gender: gender,
                    income: income,
                    age_car: carAge
                })
            });

            const result = await res.json();
            if (result.status === 'success') {
                updatePredictionUI(result.predictions);
            }
        } catch (err) {
            console.error("Prediction API failed:", err);
        }
    }

    function updatePredictionUI(predictions) {
        const lrProb = predictions['Logistic Regression'].probability;
        const dtProb = predictions['Decision Tree'].probability;
        const rfProb = predictions['Random Forest'].probability;

        // Animate meters
        document.getElementById('prob-lr-bar').style.width = (lrProb * 100) + "%";
        document.getElementById('prob-lr').innerText = Math.round(lrProb * 100) + "%";

        document.getElementById('prob-dt-bar').style.width = (dtProb * 100) + "%";
        document.getElementById('prob-dt').innerText = Math.round(dtProb * 100) + "%";

        document.getElementById('prob-rf-bar').style.width = (rfProb * 100) + "%";
        document.getElementById('prob-rf').innerText = Math.round(rfProb * 100) + "%";

        // Average consensus buying verdict
        const avg = (lrProb + dtProb + rfProb) / 3;
        const verdictBox = document.getElementById('prediction-verdict-box');
        const verdictTitle = document.getElementById('predictor-verdict-title');
        const verdictDesc = document.getElementById('predictor-verdict-desc');

        if (avg >= 0.5) {
            verdictBox.className = "overall-verdict-box buy-yes";
            verdictBox.querySelector('.verdict-icon').innerHTML = '<i class="fa-solid fa-circle-check"></i>';
            verdictTitle.innerText = `Likely to Purchase (${Math.round(avg * 100)}% Consensus)`;
            verdictDesc.innerText = "This customer matches the high-probability purchasing demographic profile. Focus conversion marketing strategies, low-interest trade-in financing, and active vehicle upgrade outreach.";
        } else {
            verdictBox.className = "overall-verdict-box buy-no";
            verdictBox.querySelector('.verdict-icon').innerHTML = '<i class="fa-solid fa-circle-xmark"></i>';
            verdictTitle.innerText = `Unlikely to Purchase (${Math.round(avg * 100)}% Consensus)`;
            verdictDesc.innerText = "This customer profile shows low purchase conversion intent. General brand awareness campaigns are recommended over high-cost targeted sales pitches.";
        }
    }

    // Initialize Dashboard
    loadDashboardData();
});

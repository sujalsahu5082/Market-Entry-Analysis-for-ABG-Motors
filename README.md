<h1>🚗 Market Entry Analysis for ABG Motors – Capstone Project</h1>

<h2>📌 Project Objective</h2>
<p>
To determine whether <b>ABG Motors</b>, a Japanese automobile manufacturer, should enter the <b>Indian market</b> by leveraging 
<b>data-driven decision-making</b>. This involves building a <b>classification model</b> using Japanese market data to predict potential 
Indian customers and evaluating profitability against a sales target of <b>12,000 cars/year</b>.
</p>

<p align="center">
  <img src="https://github.com/pratiksutar841/Market-Entry-Analysis-for-ABG-Motors-in-India---CAPSTONE-PROJECT-/blob/main/Dashboard-Photo.png" alt="Market Entry Analysis" width="800">
</p>

<hr>

<h2>🧠 Problem Statement</h2>
<p>
ABG Motors is exploring expansion opportunities in India, assuming customer behavior may be similar to Japan.
</p>
<p>You are tasked to:</p>
<ul>
    <li>Analyze sample customer data from <b>Japan</b> (training data) and <b>India</b> (prediction data).</li>
    <li>Build a <b>machine learning classification model</b> to estimate purchase likelihood.</li>
    <li>Identify the <b>number of potential Indian customers</b> and compare it against the 12,000-car sales benchmark.</li>
    <li>Provide <b>business recommendations</b> backed by predictive analytics and visualization insights.</li>
</ul>

<hr>

<h2>📂 Project Structure</h2>
<pre>
📁 ABG-Market-Entry-Analysis
│── ABG_Market_Entry_Analysis.ipynb          # Jupyter Notebook with full workflow
│── cleaned_japanese.csv                     # Cleaned Japanese dataset
│── cleaned_indian_with_predictions.csv      # Indian dataset with prediction results
│── ABG_Market_Entry_Report.docx              # Detailed project report
│── /Tableau_Charts/                          # Tableau visualizations (PNG/Screenshots)
│── README.md                                 # Project documentation
</pre>

<hr>

<h2>🛠️ Tools & Technologies</h2>
<ul>
    <li><b>Programming & Libraries:</b> Python, Pandas, NumPy, Scikit-learn, Seaborn, Matplotlib</li>
    <li><b>Data Visualization:</b> Tableau</li>
    <li><b>Environment:</b> Google Colab, Jupyter Notebook</li>
    <li><b>Version Control:</b> Git & GitHub</li>
</ul>

<hr>

<h2>📊 Methodology</h2>
<ol>
    <li><b>Data Understanding & Cleaning</b>
        <ul>
            <li>Loaded Japanese & Indian datasets</li>
            <li>Checked for missing values, duplicates, outliers</li>
            <li>Encoded categorical variables and scaled numerical features</li>
        </ul>
    </li>
    <li><b>Exploratory Data Analysis (EDA)</b>
        <ul>
            <li>Demographic patterns of buyers vs. non-buyers</li>
            <li>Correlation between age, income, marital status, and purchase decision</li>
            <li>Visual comparisons of Japan vs. India</li>
        </ul>
    </li>
    <li><b>Model Building</b>
        <ul>
            <li>Algorithm: Logistic Regression (due to interpretability)</li>
            <li>Train-test split: 70% training, 30% testing</li>
            <li>Metrics: Accuracy, Precision, Recall, F1-score, ROC-AUC</li>
        </ul>
    </li>
    <li><b>Prediction on Indian Dataset</b>
        <ul>
            <li>Applied trained model to Indian customers</li>
            <li>Counted predicted buyers and compared with target</li>
        </ul>
    </li>
    <li><b>Visualization in Tableau</b>
        <ul>
            <li>Age vs. Purchase Likelihood</li>
            <li>Income Distribution of Buyers</li>
            <li>Country-wise Sales Potential Comparison</li>
        </ul>
    </li>
</ol>

<hr>

<h2>📈 Key Results</h2>
<ul>
    <li><b>Predicted Indian Buyers:</b> 13,285 customers/year</li>
    <li><b>Target Sales:</b> 12,000 cars/year</li>
    <li><b>Recommendation:</b> ✅ <b>Proceed with Market Entry</b></li>
</ul>

<p><b>Model Performance on Japanese Data:</b></p>
<ul>
    <li>Accuracy: 85%</li>
    <li>Precision: 83%</li>
    <li>Recall: 81%</li>
    <li>F1-score: 82%</li>
    <li>ROC-AUC: 0.90</li>
</ul>

<hr>

<h2>📌 Business Insights</h2>
<ul>
    <li><b>Income</b> is the strongest predictor of car purchase likelihood.</li>
    <li>Married customers in the <b>30–50 age range</b> show the highest buying intent.</li>
    <li>Similar purchasing patterns between Japan and India validate the market similarity assumption.</li>
    <li>Sales potential exceeds the break-even benchmark by <b>10.7%</b>.</li>
</ul>

<hr>

<h2>📷 Tableau Visualizations</h2>
<ul>
    <li>Customer segmentation by age group & income</li>
    <li>Comparative sales potential in Japan vs. India</li>
    <li>Purchase likelihood distribution</li>
</ul>
<p>📁 <i>See folder:</i> <code>/Tableau_Charts</code></p>

<!-- Tableau Link -->
<p>
    🌐 <b>Interactive Dashboard:</b>  
    <a href="https://public.tableau.com/shared/SY45BDSFH?:display_count=n&:origin=viz_share_link" target="_blank">Click here to view on Tableau Public</a>
</p>

<!-- Image Preview -->
<p align="center">
    <a href="YOUR_TABLEAU_PUBLIC_LINK" target="_blank">
        <img src="https://github.com/sujalsahu5082/Market-Entry-Analysis-for-ABG-Motors-in-India---CAPSTONE-PROJECT-/blob/main/Dashboard-Photo.png" alt="Tableau Dashboard Preview" width="800">
    </a>
</p>

<hr>

<h2>✅ Final Recommendation</h2>
<p>
Based on predictive modeling and market similarity, ABG Motors should <b>enter the Indian market</b>, targeting middle-aged, higher-income customers through tailored marketing campaigns.
</p>

<hr>

<h2>🙋‍♂️ Author</h2>
<p>
<b>Sujal Sahu</b><br>
B.Tech in Computer Science & Engineering<br>
GitHub: <a href="https://github.com/sujalsahu5082">sujalsahu5082</a><br>
LinkedIn: <a href="#">https://www.linkedin.com/in/sujal-sahu-b08678294/</a>
</p>

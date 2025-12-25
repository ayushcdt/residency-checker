import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(page_title="Residency Checker", layout="centered")

st.title("🇮🇳 Indian Tax Residency Checker")
st.caption("Powered by React + Streamlit")

# --- The React Component Code (Embedded) ---
# We use Babel standalone to compile JSX on the fly.
# We use Tailwind via CDN for styling.

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Residency Checker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gray-50 p-4 flex justify-center">

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        // --- Inline Icons (replacing Lucide imports for CDN compatibility) ---
        const UserIcon = () => (
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        );
        const CheckCircleIcon = () => (
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        );
        const AlertTriangleIcon = () => (
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        );
        const InfoIcon = () => (
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        );

        // --- Main Component ---
        const ResidencyChecker = () => {
            const [currentFYDays, setCurrentFYDays] = useState('');
            const [prev4FYDays, setPrev4FYDays] = useState('');
            const [indianIncome, setIndianIncome] = useState('');
            const [meetsHistoricalRNOR, setMeetsHistoricalRNOR] = useState(false);
            const [result, setResult] = useState(null);

            const calculateResidency = () => {
                const daysCurrent = Number(currentFYDays) || 0;
                const days4Years = Number(prev4FYDays) || 0;
                const income = Number(indianIncome) || 0;
                const INCOME_THRESHOLD = 1500000;

                const basicCondA = daysCurrent >= 182;
                const basicCondB = daysCurrent >= 60 && days4Years >= 365;
                
                const isSpecialRuleCase = 
                  income > INCOME_THRESHOLD && 
                  daysCurrent >= 120 && 
                  daysCurrent < 182 && 
                  days4Years >= 365;

                let status = '';
                let explanation = '';
                let type = ''; 

                if (!basicCondA && !basicCondB && !isSpecialRuleCase) {
                  status = 'NRI (Non-Resident Indian)';
                  explanation = 'Stay in current FY is below statutory limits (182 days, or 60/120 days + 365 days history).';
                  type = 'nri';
                } else {
                  if (isSpecialRuleCase) {
                    status = 'RNOR (Resident Not Ordinarily Resident)';
                    explanation = 'Indian Income > ₹15L and stay is between 120-181 days (Special Amendment).';
                    type = 'rnor';
                  } 
                  else if (meetsHistoricalRNOR) {
                    status = 'RNOR (Resident Not Ordinarily Resident)';
                    explanation = 'Met Resident criteria, but qualifies as RNOR due to past residency history.';
                    type = 'rnor';
                  } 
                  else {
                    status = 'ROR (Resident & Ordinarily Resident)';
                    explanation = 'Met residency criteria (≥ 182 days or 60+365) and does not qualify for RNOR relief.';
                    type = 'resident';
                  }
                }
                setResult({ status, explanation, type });
            };

            useEffect(() => {
                calculateResidency();
            }, [currentFYDays, prev4FYDays, indianIncome, meetsHistoricalRNOR]);

            const getStatusColor = (type) => {
                switch (type) {
                case 'nri': return 'bg-green-50 border-green-200 text-green-800';
                case 'rnor': return 'bg-orange-50 border-orange-200 text-orange-800';
                case 'resident': return 'bg-blue-50 border-blue-200 text-blue-800';
                default: return 'bg-gray-50 border-gray-200 text-gray-800';
                }
            };

            return (
                <div className="max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg border border-gray-100 font-sans">
                <div className="mb-6 flex items-center gap-2 border-b pb-4">
                    <div className="p-2 bg-indigo-600 rounded-lg">
                        <UserIcon />
                    </div>
                    <div className="text-left">
                        <h2 className="text-xl font-bold text-gray-800 m-0">Residency Status</h2>
                        <p className="text-xs text-gray-500 m-0">Based on Income Tax Act, 1961 (Sec 6)</p>
                    </div>
                </div>

                <div className="space-y-5">
                    <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1 text-left">
                        Days stayed in India (Current FY)
                    </label>
                    <input
                        type="number"
                        value={currentFYDays}
                        onChange={(e) => setCurrentFYDays(e.target.value)}
                        placeholder="e.g., 182"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                    />
                    </div>

                    <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1 text-left">
                        Days stayed in preceding 4 FYs
                    </label>
                    <input
                        type="number"
                        value={prev4FYDays}
                        onChange={(e) => setPrev4FYDays(e.target.value)}
                        placeholder="e.g., 365"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                    />
                    </div>

                    <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1 text-left">
                        Total Indian-Sourced Income (₹)
                    </label>
                    <div className="relative">
                        <input
                        type="number"
                        value={indianIncome}
                        onChange={(e) => setIndianIncome(e.target.value)}
                        placeholder="e.g., 1600000"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                        />
                    </div>
                    </div>

                    <div className="bg-gray-50 p-3 rounded-lg border border-gray-200">
                    <label className="flex items-start gap-3 cursor-pointer">
                        <input 
                        type="checkbox" 
                        checked={meetsHistoricalRNOR}
                        onChange={(e) => setMeetsHistoricalRNOR(e.target.checked)}
                        className="mt-1 w-4 h-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                        />
                        <div className="text-sm text-gray-600 text-left">
                        <span className="font-semibold text-gray-700">Historical RNOR Check:</span>
                        <br/>
                        Check this if you stayed ≤ 729 days in the last 7 years OR were NRI in 9 of the last 10 years.
                        </div>
                    </label>
                    </div>

                    {result && (
                    <div className={`mt-6 p-4 rounded-lg border flex flex-col gap-2 ${getStatusColor(result.type)}`}>
                        <div className="flex items-center gap-2">
                        {result.type === 'nri' ? <CheckCircleIcon /> : <AlertTriangleIcon />}
                        <h3 className="text-lg font-bold m-0">{result.status}</h3>
                        </div>
                        <div className="flex items-start gap-2">
                        <InfoIcon />
                        <p className="text-sm font-medium opacity-90 leading-relaxed text-left m-0">
                            {result.explanation}
                        </p>
                        </div>
                    </div>
                    )}
                </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<ResidencyChecker />);
    </script>
</body>
</html>
"""

# Render the HTML in Streamlit
components.html(html_code, height=750, scrolling=True)
import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(page_title="US Tax Residency Calculator", layout="centered")

st.title("🇺🇸 US Tax Residency Calculator")
st.caption("Substantial Presence Test (SPT) for H1B, F1, J1, L1")

# --- The React Component Code (Embedded) ---
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>US Residency Checker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body class="bg-gray-50 p-4 flex justify-center">

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;

        // --- Icons (Inline SVGs) ---
        const CalculatorIcon = () => (
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="16" y1="14" x2="16" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/></svg>
        );
        const AlertCircleIcon = ({className}) => (
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        );
        const FileTextIcon = () => (
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></svg>
        );
        const CheckCircleIcon = ({className}) => (
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        );
        const CalendarIcon = () => (
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        );

        // --- Main Logic Component ---
        const USResidencyStatus = () => {
            const [visaType, setVisaType] = useState('H1B');
            const [exemptYearsUsed, setExemptYearsUsed] = useState(''); 
            const [daysCY, setDaysCY] = useState('');
            const [daysCY1, setDaysCY1] = useState('');
            const [daysCY2, setDaysCY2] = useState('');
            
            const [result, setResult] = useState(null);
            const [sptDetails, setSptDetails] = useState(null);

            const calculateUSResidency = () => {
                const dCY = Number(daysCY) || 0;
                const dCY1 = Number(daysCY1) || 0;
                const dCY2 = Number(daysCY2) || 0;
                const yearsUsed = Number(exemptYearsUsed) || 0;

                let isExempt = false;
                let exemptionReason = '';

                // Exempt Individual Logic
                if (visaType === 'F1') {
                    if (yearsUsed < 5) {
                        isExempt = true;
                        exemptionReason = 'F1 Student status (within first 5 calendar years). Days do not count toward SPT.';
                    }
                } else if (visaType === 'J1') {
                    if (yearsUsed < 2) {
                        isExempt = true;
                        exemptionReason = 'J1 Teacher/Trainee status (within first 2 calendar years). Days do not count toward SPT.';
                    }
                }

                if (isExempt) {
                    setResult({
                        status: 'Non-Resident Alien (NRA)',
                        form: 'Form 1040-NR',
                        type: 'nra',
                        reason: exemptionReason
                    });
                    setSptDetails(null);
                    return; 
                }

                // Substantial Presence Test (SPT)
                
                // 1. 31 Day Rule
                if (dCY < 31) {
                    setResult({
                        status: 'Non-Resident Alien (NRA)',
                        form: 'Form 1040-NR',
                        type: 'nra',
                        reason: 'Present less than 31 days in the current year. Automatic Non-Resident.'
                    });
                    setSptDetails(null);
                    return;
                }

                // 2. 183 Day Weighted Rule
                const weightedTotal = dCY + (dCY1 * (1/3)) + (dCY2 * (1/6));
                const roundedTotal = weightedTotal.toFixed(1);

                setSptDetails({
                    total: roundedTotal,
                    threshold: 183,
                    passed: weightedTotal >= 183
                });

                if (weightedTotal >= 183) {
                    setResult({
                        status: 'Resident Alien (RA)',
                        form: 'Form 1040',
                        type: 'ra',
                        reason: `Met the Substantial Presence Test threshold (Total score: ${roundedTotal} ≥ 183).`
                    });
                } else {
                    setResult({
                        status: 'Non-Resident Alien (NRA)',
                        form: 'Form 1040-NR',
                        type: 'nra',
                        reason: `Did not meet the 183-day weighted threshold (Total score: ${roundedTotal}).`
                    });
                }
            };

            useEffect(() => {
                calculateUSResidency();
            }, [visaType, exemptYearsUsed, daysCY, daysCY1, daysCY2]);

            const getStatusStyles = (type) => {
                if (type === 'ra') return 'bg-blue-50 border-blue-200 text-blue-900';
                if (type === 'nra') return 'bg-green-50 border-green-200 text-green-900';
                return 'bg-gray-50 border-gray-200';
            };

            return (
                <div className="max-w-xl mx-auto p-6 bg-white rounded-xl shadow-xl border border-gray-100 font-sans">
                {/* Header */}
                <div className="mb-6 flex items-start gap-3 border-b pb-4">
                    <div className="p-2 bg-red-600 rounded-lg mt-1">
                        <CalculatorIcon />
                    </div>
                    <div className="text-left">
                        <h2 className="text-2xl font-bold text-gray-900 m-0">US Tax Residency Calculator</h2>
                        <p className="text-sm text-gray-500 m-0">Substantial Presence Test (SPT) & Exemptions.</p>
                        <div className="flex items-center gap-1 mt-2 text-xs text-red-600 bg-red-50 p-1 rounded font-semibold w-fit">
                            <AlertCircleIcon className="w-4 h-4" />
                            Warning: Visa Status ≠ Tax Status
                        </div>
                    </div>
                </div>

                <div className="space-y-6">
                    
                    {/* Inputs */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-bold text-gray-700 mb-1 text-left">Current Visa Type</label>
                        <select
                        value={visaType}
                        onChange={(e) => setVisaType(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                        >
                        <option value="H1B">H1B (Specialty Occupation)</option>
                        <option value="L1">L1 (Intracompany Transferee)</option>
                        <option value="F1">F1 (Student)</option>
                        <option value="J1">J1 (Teacher/Trainee)</option>
                        </select>
                    </div>

                    {(visaType === 'F1' || visaType === 'J1') && (
                        <div>
                        <label className="block text-sm font-bold text-gray-700 mb-1 text-left">
                        Previous exempt years?
                        <span className="block text-xs font-normal text-gray-500">How many previous calendar years were you on F/J status?</span>
                        </label>
                        <input
                        type="number"
                        min="0"
                        value={exemptYearsUsed}
                        onChange={(e) => setExemptYearsUsed(e.target.value)}
                        placeholder="e.g., 2"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                        />
                    </div>
                    )}
                    </div>

                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                        <h3 className="text-sm font-bold text-gray-800 mb-3 flex items-center gap-2">
                        <CalendarIcon /> Days Present in US
                        </h3>
                        <div className="grid grid-cols-3 gap-3">
                            <div>
                                <label className="block text-xs font-semibold text-gray-600 mb-1 text-left">Current Year (CY)</label>
                                <input type="number" min="0" value={daysCY} onChange={(e) => setDaysCY(e.target.value)} placeholder="150"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 outline-none text-sm" />
                                <span className="text-xs text-gray-400 block mt-1 text-left">Counts 100%</span>
                            </div>
                            <div>
                                <label className="block text-xs font-semibold text-gray-600 mb-1 text-left">Last Year</label>
                                <input type="number" min="0" value={daysCY1} onChange={(e) => setDaysCY1(e.target.value)} placeholder="300"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 outline-none text-sm" />
                                <span className="text-xs text-gray-400 block mt-1 text-left">Counts ~33%</span>
                            </div>
                            <div>
                                <label className="block text-xs font-semibold text-gray-600 mb-1 text-left">Year Before</label>
                                <input type="number" min="0" value={daysCY2} onChange={(e) => setDaysCY2(e.target.value)} placeholder="365"
                                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 outline-none text-sm" />
                                <span className="text-xs text-gray-400 block mt-1 text-left">Counts ~17%</span>
                            </div>
                        </div>
                    </div>

                    {/* Output */}
                    {result && (
                    <div className={`p-5 rounded-xl border-2 ${getStatusStyles(result.type)} transition-all duration-300`}>
                        <div className="flex items-center justify-between mb-3">
                        <div className="text-left">
                            <h3 className="text-2xl font-extrabold uppercase tracking-tight m-0">{result.status}</h3>
                            <p className="text-md opacity-90 flex items-center gap-1 mt-1 font-semibold m-0">
                                <FileTextIcon /> You file: {result.form}
                            </p>
                        </div>
                        {result.type === 'ra' 
                            ? <AlertCircleIcon className="w-12 h-12 opacity-80 text-blue-700" /> 
                            : <CheckCircleIcon className="w-12 h-12 opacity-80 text-green-700" />
                        }
                        </div>
                        
                        <div className="bg-white/60 p-3 rounded-lg text-sm mb-3 text-left">
                        <span className="font-bold">Reason: </span> {result.reason}
                        </div>

                        {sptDetails && (
                        <div className="mt-4 pt-4 border-t border-black/10 text-sm">
                            <h4 className="font-bold mb-2 text-left">Substantial Presence Test Score:</h4>
                            <div className="flex items-center justify-between bg-white/70 p-2 rounded">
                                <span>Your Weighted Score: <strong>{sptDetails.total}</strong></span>
                                <span className="text-gray-500">Threshold: {sptDetails.threshold}</span>
                            </div>
                            <div className="w-full bg-gray-300 h-3 rounded-full mt-2 overflow-hidden relative">
                                <div 
                                    className={`h-full ${sptDetails.passed ? 'bg-blue-600' : 'bg-green-500'} transition-all duration-500 relative`} 
                                    style={{width: `${Math.min((sptDetails.total / 200) * 100, 100)}%`}}
                                ></div>
                                <div className="absolute top-0 bottom-0 w-0.5 bg-red-500" style={{left: `${(183/200)*100}%`}} title="183 Day Threshold"></div>
                            </div>
                        </div>
                        )}
                    </div>
                    )}
                </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<USResidencyStatus />);
    </script>
</body>
</html>
"""

components.html(html_code, height=800, scrolling=True)
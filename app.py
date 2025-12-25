import streamlit as st
import streamlit.components.v1 as components

# Page Config
st.set_page_config(page_title="US Tax Residency Calculator", layout="wide")

# Hide standard Streamlit chrome for a cleaner look
st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- React Application Code ---
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>US Residency Calculator</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
        /* Custom scrollbar for cleanliness */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    </style>
</head>
<body class="p-4 md:p-8 flex justify-center items-start min-h-screen">

    <div id="root" class="w-full max-w-4xl"></div>

    <script type="text/babel">
        const { useState, useEffect, useMemo } = React;

        // --- Icons ---
        const PlusIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>;
        const TrashIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>;
        const CalendarIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>;
        const AlertIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-amber-500"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>;
        const CheckIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" className="text-green-600"><polyline points="20 6 9 17 4 12"/></svg>;
        const XCircleIcon = () => <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-600"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>;

        // --- Helper: Date Difference ---
        const getDaysDiff = (start, end) => {
            if (!start || !end) return 0;
            const s = new Date(start);
            const e = new Date(end);
            if (isNaN(s) || isNaN(e)) return 0;
            // Difference in time / milliseconds per day
            const diffTime = Math.abs(e - s);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
            return diffDays + 1; // Include both start and end dates
        };

        // --- Helper Component: Year Trip Manager ---
        const YearTripManager = ({ label, yearLabel, trips, setTrips, weight }) => {
            const addTrip = () => {
                setTrips([...trips, { start: '', end: '', id: Date.now() }]);
            };

            const removeTrip = (id) => {
                setTrips(trips.filter(t => t.id !== id));
            };

            const updateTrip = (id, field, value) => {
                setTrips(trips.map(t => t.id === id ? { ...t, [field]: value } : t));
            };

            const totalDays = trips.reduce((acc, t) => acc + getDaysDiff(t.start, t.end), 0);

            return (
                <div className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300">
                    <div className="bg-gray-50 px-5 py-3 border-b border-gray-100 flex justify-between items-center">
                        <div>
                            <h3 className="text-sm font-bold text-gray-700 uppercase tracking-wide">{label}</h3>
                            <p className="text-xs text-gray-500">{yearLabel}</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="text-xs font-medium px-2 py-1 bg-gray-200 rounded text-gray-600">Weight: {weight}</span>
                            <span className="text-sm font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100">
                                {totalDays} Days
                            </span>
                        </div>
                    </div>
                    
                    <div className="p-4 space-y-3">
                        {trips.length === 0 ? (
                            <div className="text-center py-6 text-gray-400 text-sm border-2 border-dashed border-gray-100 rounded-lg">
                                No trips added for this year.
                            </div>
                        ) : (
                            trips.map((trip, idx) => {
                                const days = getDaysDiff(trip.start, trip.end);
                                return (
                                    <div key={trip.id} className="flex items-end gap-3 animate-fade-in">
                                        <div className="flex-1">
                                            <label className="text-[10px] uppercase font-bold text-gray-400 mb-1 block">Start Date</label>
                                            <input 
                                                type="date" 
                                                className="w-full text-sm p-2 bg-gray-50 border border-gray-200 rounded focus:ring-2 focus:ring-indigo-500 outline-none"
                                                value={trip.start}
                                                onChange={(e) => updateTrip(trip.id, 'start', e.target.value)}
                                            />
                                        </div>
                                        <div className="flex-1">
                                            <label className="text-[10px] uppercase font-bold text-gray-400 mb-1 block">End Date</label>
                                            <input 
                                                type="date" 
                                                className="w-full text-sm p-2 bg-gray-50 border border-gray-200 rounded focus:ring-2 focus:ring-indigo-500 outline-none"
                                                value={trip.end}
                                                onChange={(e) => updateTrip(trip.id, 'end', e.target.value)}
                                            />
                                        </div>
                                        <div className="w-16 text-center pb-2">
                                            <span className="text-xs font-semibold text-gray-600">{days > 0 ? days : '-'} d</span>
                                        </div>
                                        <button 
                                            onClick={() => removeTrip(trip.id)}
                                            className="p-2.5 mb-[1px] text-gray-400 hover:text-red-500 hover:bg-red-50 rounded transition-colors"
                                        >
                                            <TrashIcon />
                                        </button>
                                    </div>
                                );
                            })
                        )}
                        
                        <button 
                            onClick={addTrip}
                            className="w-full py-2 flex items-center justify-center gap-2 text-sm font-medium text-indigo-600 bg-white border border-indigo-100 rounded-lg hover:bg-indigo-50 transition-colors"
                        >
                            <PlusIcon /> Add Trip
                        </button>
                    </div>
                </div>
            );
        };

        // --- Main Application ---
        const App = () => {
            const [visaType, setVisaType] = useState('H1B');
            const [exemptYears, setExemptYears] = useState(0);
            
            // Trips State
            const [tripsCY, setTripsCY] = useState([]);
            const [tripsCY1, setTripsCY1] = useState([]);
            const [tripsCY2, setTripsCY2] = useState([]);

            const [result, setResult] = useState(null);

            // Calculation Logic
            useEffect(() => {
                // 1. Check Exempt Status
                let isExempt = false;
                let exemptReason = '';

                if (visaType === 'F1' && exemptYears < 5) {
                    isExempt = true;
                    exemptReason = 'F1 Student (First 5 calendar years are exempt from SPT)';
                } else if (visaType === 'J1' && exemptYears < 2) {
                    isExempt = true;
                    exemptReason = 'J1 Teacher/Trainee (First 2 calendar years are exempt from SPT)';
                }

                if (isExempt) {
                    setResult({
                        status: 'Non-Resident Alien',
                        code: 'NRA',
                        form: 'Form 1040-NR',
                        reason: exemptReason,
                        isExempt: true
                    });
                    return;
                }

                // 2. Calculate Days
                const daysCY = tripsCY.reduce((acc, t) => acc + getDaysDiff(t.start, t.end), 0);
                const daysCY1 = tripsCY1.reduce((acc, t) => acc + getDaysDiff(t.start, t.end), 0);
                const daysCY2 = tripsCY2.reduce((acc, t) => acc + getDaysDiff(t.start, t.end), 0);

                // 3. Apply SPT Logic
                if (daysCY < 31) {
                    setResult({
                        status: 'Non-Resident Alien',
                        code: 'NRA',
                        form: 'Form 1040-NR',
                        reason: 'Present less than 31 days in current year.',
                        score: daysCY,
                        isExempt: false
                    });
                    return;
                }

                const weightedScore = daysCY + (daysCY1 / 3) + (daysCY2 / 6);
                const passed = weightedScore >= 183;

                setResult({
                    status: passed ? 'Resident Alien' : 'Non-Resident Alien',
                    code: passed ? 'RA' : 'NRA',
                    form: passed ? 'Form 1040' : 'Form 1040-NR',
                    reason: passed ? 'Passed Substantial Presence Test (≥ 183 days).' : 'Failed Substantial Presence Test (< 183 days).',
                    score: weightedScore.toFixed(1),
                    details: { daysCY, daysCY1, daysCY2 },
                    isExempt: false,
                    passed
                });

            }, [visaType, exemptYears, tripsCY, tripsCY1, tripsCY2]);

            return (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 font-sans text-gray-800">
                    
                    {/* Left Column: Inputs */}
                    <div className="lg:col-span-7 space-y-6">
                        
                        {/* 1. Profile Section */}
                        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                                <span className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600"><CalendarIcon /></span>
                                Profile & Visa
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Visa Type</label>
                                    <select 
                                        value={visaType} 
                                        onChange={(e) => setVisaType(e.target.value)}
                                        className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg font-medium focus:ring-2 focus:ring-blue-500 outline-none transition"
                                    >
                                        <option value="H1B">H1B (Specialty Occupation)</option>
                                        <option value="L1">L1 (Intracompany)</option>
                                        <option value="F1">F1 (Student)</option>
                                        <option value="J1">J1 (Teacher/Trainee)</option>
                                    </select>
                                </div>
                                {(visaType === 'F1' || visaType === 'J1') && (
                                    <div className="animate-fade-in">
                                        <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Prior Exempt Years</label>
                                        <input 
                                            type="number" 
                                            min="0"
                                            value={exemptYears}
                                            onChange={(e) => setExemptYears(e.target.value)}
                                            className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg font-medium focus:ring-2 focus:ring-blue-500 outline-none transition"
                                        />
                                        <p className="text-[10px] text-gray-400 mt-1">Calendar years already spent on F/J status.</p>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* 2. Trip Calculator (Hidden if Exempt) */}
                        {result && result.isExempt ? (
                            <div className="bg-blue-50 border border-blue-100 rounded-2xl p-8 text-center">
                                <p className="text-blue-800 font-medium">
                                    You are currently an Exempt Individual.
                                </p>
                                <p className="text-blue-600 text-sm mt-1">
                                    You do not need to count your days for the Substantial Presence Test.
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-4 animate-fade-in">
                                <div className="flex items-center justify-between">
                                    <h2 className="text-lg font-bold text-gray-800">Travel History</h2>
                                    <p className="text-xs text-gray-400">Add all US visits for calculation</p>
                                </div>
                                <YearTripManager 
                                    label="Current Year" 
                                    yearLabel="(Tax Year)" 
                                    weight="100%" 
                                    trips={tripsCY} 
                                    setTrips={setTripsCY} 
                                />
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <YearTripManager 
                                        label="Last Year" 
                                        yearLabel="(CY - 1)" 
                                        weight="~33%" 
                                        trips={tripsCY1} 
                                        setTrips={setTripsCY1} 
                                    />
                                    <YearTripManager 
                                        label="Year Before" 
                                        yearLabel="(CY - 2)" 
                                        weight="~17%" 
                                        trips={tripsCY2} 
                                        setTrips={setTripsCY2} 
                                    />
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Right Column: Results Sticky */}
                    <div className="lg:col-span-5">
                        <div className="sticky top-4">
                            {result && (
                                <div className={`rounded-3xl shadow-lg border overflow-hidden transition-all duration-500 ${
                                    result.code === 'RA' ? 'bg-white border-blue-100' : 'bg-white border-green-100'
                                }`}>
                                    {/* Result Header */}
                                    <div className={`p-8 text-center ${
                                        result.code === 'RA' ? 'bg-gradient-to-br from-blue-600 to-indigo-700 text-white' : 'bg-gradient-to-br from-emerald-500 to-teal-600 text-white'
                                    }`}>
                                        <div className="bg-white/20 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 backdrop-blur-sm">
                                            {result.code === 'RA' ? <AlertIcon className="text-white" /> : <CheckIcon className="text-white" />}
                                        </div>
                                        <h3 className="text-3xl font-bold mb-1">{result.status}</h3>
                                        <p className="opacity-90 font-medium text-lg">{result.form}</p>
                                    </div>

                                    {/* Result Body */}
                                    <div className="p-6 space-y-6">
                                        <div>
                                            <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Reasoning</h4>
                                            <p className="text-sm text-gray-700 leading-relaxed font-medium bg-gray-50 p-3 rounded-lg border border-gray-100">
                                                {result.reason}
                                            </p>
                                        </div>

                                        {!result.isExempt && (
                                            <div>
                                                <div className="flex justify-between items-end mb-2">
                                                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">SPT Score</h4>
                                                    <span className="text-2xl font-bold text-gray-800">{result.score}</span>
                                                </div>
                                                
                                                {/* Progress Bar */}
                                                <div className="relative h-4 bg-gray-100 rounded-full overflow-hidden">
                                                    <div 
                                                        className={`absolute top-0 left-0 h-full transition-all duration-1000 ${
                                                            result.passed ? 'bg-blue-600' : 'bg-emerald-500'
                                                        }`}
                                                        style={{ width: `${Math.min((result.score / 200) * 100, 100)}%` }}
                                                    ></div>
                                                    {/* 183 Marker */}
                                                    <div className="absolute top-0 bottom-0 w-0.5 bg-red-400 z-10" style={{ left: `${(183/200)*100}%` }}></div>
                                                </div>
                                                <div className="flex justify-between text-[10px] text-gray-400 mt-1 font-medium">
                                                    <span>0 Days</span>
                                                    <span className="text-red-500">Threshold: 183 Days</span>
                                                    <span>200+ Days</span>
                                                </div>
                                            </div>
                                        )}
                                        
                                        <div className="bg-amber-50 border border-amber-100 p-3 rounded-lg flex gap-3 items-start">
                                            <div className="mt-0.5"><AlertIcon /></div>
                                            <p className="text-xs text-amber-800 leading-relaxed">
                                                <strong>Disclaimer:</strong> This tool is for estimation only. Tax laws are complex. Consult a CPA for official filing.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
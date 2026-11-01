import React, { useState, useEffect } from 'react';
import { Clock, MapPin, User, ChevronRight, AlertTriangle, Info, BookOpen, AlertCircle, FileText } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, Cell } from 'recharts';
import { fetchFacultyDashboard } from '../lib/api';

const DEFAULT_FACULTY_DATA = {
  faculty_info: {
    id: "FAC_DEMO_01",
    name: "Dr. Demo Faculty",
    email: "faculty@college.edu",
    department: "Computer Science and Engineering",
    designation: "Assistant Professor",
    office: "Block B — Room 204",
    office_hours: "Mon–Wed 3:00 PM – 4:00 PM",
    specializations: ["Artificial Intelligence", "Machine Learning"]
  },
  teaching_overview: {
    courses_count: 4,
    sections_count: 6,
    total_students: 182,
    weekly_hours: 16,
    avg_attendance_pct: 86.7,
    pending_tasks_count: 12,
    urgent_tasks_count: 4
  },
  today_schedule: [
    {
      time: "09:00 AM - 10:15 AM",
      course: "Artificial Intelligence (AI301)",
      room: "Room C-204",
      section: "CSE-B",
      enrolled: 42,
      status: "ongoing"
    },
    {
      time: "11:00 AM - 12:15 PM",
      course: "Machine Learning (AI303)",
      room: "AI Lab 2",
      section: "CSE-A",
      enrolled: 38,
      status: "upcoming"
    },
    {
      time: "02:00 PM - 03:15 PM",
      course: "Data Structures & Algorithms (CS201)",
      room: "Room B-302",
      section: "CSE-C",
      enrolled: 45,
      status: "upcoming"
    }
  ],
  attendance_analytics: [
    { course: "Artificial Intelligence", section: "CSE-A", pct: 91, status: "healthy" },
    { course: "Machine Learning", section: "CSE-B", pct: 84, status: "monitor" },
    { course: "Data Structures", section: "CSE-A", pct: 89, status: "healthy" },
    { course: "Database Management Systems", section: "CSE-C", pct: 73, status: "attention" }
  ],
  class_performance: [
    { course: "Artificial Intelligence", avg_score: 82 },
    { course: "Machine Learning", avg_score: 76 },
    { course: "Data Structures", avg_score: 85 },
    { course: "DBMS", avg_score: 68 }
  ],
  assessment_status: {
    completed: ["AI301 Midterm I", "CS201 Midterm I"],
    pending: [
      { task: "ML Midterm Papers", count: 12 },
      { task: "DBMS Lab Records", count: 8 },
      { task: "AI Assignment 3", count: 28 }
    ]
  },
  student_alerts: [
    { type: "attendance", severity: "warning", message: "8 students below 75% attendance" },
    { type: "performance", severity: "danger", message: "5 students scored below 40% in Midterm 1" },
    { type: "absence", severity: "danger", message: "3 students missed 3 consecutive lectures" },
    { type: "submission", severity: "info", message: "12 students pending Assignment 3 submission" }
  ],
  pending_actions: [
    { id: 1, title: "Grade 28 AI Assignments", due: "Today", priority: "urgent" },
    { id: 2, title: "Enter ML Midterm marks (12 students)", due: "Tomorrow", priority: "urgent" },
    { id: 3, title: "Submit AI Attendance log", due: "Today", priority: "normal" },
    { id: 4, title: "Upload DBMS Unit 4 Slides", due: "Oct 02", priority: "due_soon" }
  ],
  courses: [
    { code: "AI301", name: "Artificial Intelligence", section: "CSE-A", students: 42, attendance: 91, avg_marks: 82 },
    { code: "AI303", name: "Machine Learning", section: "CSE-B", students: 38, attendance: 84, avg_marks: 76 },
    { code: "CS201", name: "Data Structures", section: "CSE-C", students: 45, attendance: 89, avg_marks: 85 },
    { code: "CS304", name: "Database Management Systems", section: "CSE-C", students: 57, attendance: 73, avg_marks: 68 }
  ]
};

export default function FacultyDashboard({ user, setDrawerState }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const facultyId = user?.id || user?.username || 'FAC_DEMO_01';
    fetchFacultyDashboard(facultyId)
      .then(res => {
        setData(res || DEFAULT_FACULTY_DATA);
        setLoading(false);
      })
      .catch(err => {
        console.warn("Using verified faculty dashboard fallback:", err?.message || err);
        // Fallback directly so the dashboard NEVER gets stuck on loading
        setData(DEFAULT_FACULTY_DATA);
        setLoading(false);
      });
  }, [user]);

  if (loading && !data) {
    return (
      <div className="flex flex-col justify-center items-center h-64 gap-3">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-sky-500"></div>
        <div className="animate-pulse text-sky-500 font-bold text-lg">Loading Faculty Dashboard...</div>
      </div>
    );
  }

  const activeData = data || DEFAULT_FACULTY_DATA;
  const {
    faculty_info,
    teaching_overview,
    today_schedule,
    attendance_analytics,
    class_performance,
    assessment_status,
    student_alerts,
    pending_actions,
    courses
  } = activeData;

  const performanceColors = ['#38bdf8', '#818cf8', '#34d399', '#fbbf24'];

  return (
    <div className="space-y-6 animate-float-slow" style={{ animationDuration: '8s' }}>
      
      {/* Row 1: Today's Schedule & Teaching KPI Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Today's Schedule */}
        <div className="glass-card p-6 rounded-3xl col-span-1 lg:col-span-2 relative overflow-hidden">
          <div className="absolute -top-10 -right-10 w-32 h-32 bg-sky-200/50 rounded-full blur-2xl"></div>
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-semibold text-primary">Today's Schedule ⏰</h3>
            <button onClick={() => setDrawerState && setDrawerState(prev => ({...prev, timetable: true}))} className="text-sm font-semibold text-sky-600 hover:text-sky-700 flex items-center gap-1 bg-sky-50 px-3 py-1.5 rounded-full transition">
              View Full Timetable 🗓️ <ChevronRight size={16}/>
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {today_schedule?.map((cls, i) => (
              <div key={i} className="p-4 rounded-2xl bg-white/60 border border-white/80 shadow-sm hover:shadow-md transition flex flex-col h-full relative">
                <div className="absolute top-4 right-4 flex items-center">
                  <span className={`w-2.5 h-2.5 rounded-full ${cls.status === 'ongoing' ? 'bg-green-500 animate-pulse' : cls.status === 'upcoming' ? 'bg-sky-500' : 'bg-slate-300'}`}></span>
                </div>
                <div className="text-xs font-bold text-sky-600 mb-1 flex items-center gap-1"><Clock size={12}/> {cls.time}</div>
                <div className="font-bold text-slate-800 text-sm mt-1">{cls.course}</div>
                <div className="text-xs text-slate-500 mb-3 font-semibold">Section: {cls.section}</div>
                <div className="flex items-center justify-between mt-auto pt-2 border-t border-slate-100">
                  <span className="text-[10px] flex items-center gap-1 text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded-md truncate"><MapPin size={10}/> {cls.room}</span>
                  <span className="text-[10px] flex items-center gap-1 text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded-md"><User size={10}/> {cls.enrolled} Enrolled</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Teaching Overview KPIs */}
        <div className="glass-card p-6 rounded-3xl flex flex-col justify-center">
           <h3 className="text-lg font-semibold text-primary mb-4">Teaching Overview</h3>
           <div className="grid grid-cols-2 gap-3">
              <div className="bg-white/60 border border-white/80 p-3 rounded-2xl text-center shadow-sm">
                <div className="text-xl mb-1">📚</div>
                <div className="font-bold text-slate-800 text-sm">{teaching_overview?.courses_count} Courses</div>
                <div className="text-[10px] text-slate-500 font-semibold">{teaching_overview?.sections_count} Sections</div>
              </div>
              <div className="bg-white/60 border border-white/80 p-3 rounded-2xl text-center shadow-sm">
                <div className="text-xl mb-1">👥</div>
                <div className="font-bold text-slate-800 text-sm">{teaching_overview?.total_students} Students</div>
                <div className="text-[10px] text-slate-500 font-semibold">Total Assigned</div>
              </div>
              <div className="bg-white/60 border border-white/80 p-3 rounded-2xl text-center shadow-sm">
                <div className="text-xl mb-1">📊</div>
                <div className="font-bold text-slate-800 text-sm">{teaching_overview?.avg_attendance_pct}%</div>
                <div className="text-[10px] text-green-600 font-semibold">+2.4% Avg Att.</div>
              </div>
              <div className="bg-white/60 border border-white/80 p-3 rounded-2xl text-center shadow-sm relative">
                {teaching_overview?.urgent_tasks_count > 0 && <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">{teaching_overview.urgent_tasks_count} Urgent</span>}
                <div className="text-xl mb-1">📝</div>
                <div className="font-bold text-slate-800 text-sm">{teaching_overview?.pending_tasks_count} Tasks</div>
                <div className="text-[10px] text-slate-500 font-semibold">Pending Actions</div>
              </div>
           </div>
        </div>
      </div>

      {/* Row 2: Attendance Analytics & Class Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Attendance Analytics */}
        <div className="glass-card p-6 rounded-3xl">
          <h3 className="text-lg font-semibold text-primary mb-4">Attendance Analytics 📌</h3>
          <div className="space-y-4">
            {attendance_analytics?.map((att, i) => (
              <div key={i} className="bg-white/50 p-3 rounded-xl border border-white">
                <div className="flex justify-between items-center mb-1">
                  <div className="font-semibold text-sm text-slate-700">{att.course} <span className="text-xs text-slate-400">({att.section})</span></div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-800">{att.pct}%</span>
                    {att.status === 'healthy' && <span className="bg-green-100 text-green-700 text-[10px] font-bold px-2 py-0.5 rounded-full">Healthy</span>}
                    {att.status === 'monitor' && <span className="bg-amber-100 text-amber-700 text-[10px] font-bold px-2 py-0.5 rounded-full">Monitor</span>}
                    {att.status === 'attention' && <span className="bg-red-100 text-red-700 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1"><AlertTriangle size={10}/> Attention Required</span>}
                  </div>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-1.5">
                  <div className={`h-1.5 rounded-full ${att.status === 'attention' ? 'bg-red-500' : att.status === 'monitor' ? 'bg-amber-500' : 'bg-green-500'}`} style={{ width: `${att.pct}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Class Performance */}
        <div className="glass-card p-6 rounded-3xl flex flex-col">
          <h3 className="text-lg font-semibold text-primary mb-4">Class Performance 📉</h3>
          <div className="flex-1 min-h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={class_performance} margin={{ top: 0, right: 30, left: 0, bottom: 0 }}>
                <XAxis type="number" domain={[0, 100]} hide />
                <YAxis dataKey="course" type="category" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 11, width: 80}} width={90} />
                <RechartsTooltip cursor={{fill: 'rgba(0,0,0,0.05)'}} contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 10px 25px rgba(0,0,0,0.1)'}} />
                <Bar dataKey="avg_score" radius={[0, 4, 4, 0]} barSize={20}>
                  {class_performance?.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={performanceColors[index % performanceColors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Row 3: Pending Academic Actions & Student Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Pending Actions */}
        <div className="glass-card p-6 rounded-3xl">
          <h3 className="text-lg font-semibold text-primary mb-4">Pending Actions ✓</h3>
          <div className="space-y-3">
            {pending_actions?.map(action => (
              <div key={action.id} className="flex items-center gap-3 bg-white/60 p-3 rounded-xl border border-white hover:bg-white transition cursor-pointer">
                <div className="w-5 h-5 rounded border border-slate-300 flex-shrink-0 flex items-center justify-center bg-white"><div className="w-3 h-3 rounded-sm hover:bg-sky-400 transition"></div></div>
                <div className="flex-1">
                  <div className="font-semibold text-sm text-slate-800">{action.title}</div>
                  <div className="text-xs text-slate-500 flex items-center gap-1"><Clock size={10}/> Due: {action.due}</div>
                </div>
                <div>
                  {action.priority === 'urgent' && <span className="bg-red-100 text-red-600 border border-red-200 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">🔴 Urgent</span>}
                  {action.priority === 'due_soon' && <span className="bg-amber-100 text-amber-600 border border-amber-200 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">🟠 Due Soon</span>}
                  {action.priority === 'normal' && <span className="bg-blue-100 text-blue-600 border border-blue-200 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">🔵 Normal</span>}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Student Alerts */}
        <div className="glass-card p-6 rounded-3xl">
          <h3 className="text-lg font-semibold text-primary mb-4">Student Alerts ⚠️</h3>
          <div className="space-y-3">
            {student_alerts?.map((alert, i) => (
              <div key={i} className={`flex items-start gap-3 p-3 rounded-xl border ${alert.severity === 'danger' ? 'bg-red-50 border-red-100' : alert.severity === 'warning' ? 'bg-amber-50 border-amber-100' : 'bg-blue-50 border-blue-100'}`}>
                <div className={`mt-0.5 ${alert.severity === 'danger' ? 'text-red-500' : alert.severity === 'warning' ? 'text-amber-500' : 'text-blue-500'}`}>
                  {alert.severity === 'danger' ? <AlertCircle size={16} /> : alert.severity === 'warning' ? <AlertTriangle size={16}/> : <Info size={16}/>}
                </div>
                <div className={`text-sm font-medium ${alert.severity === 'danger' ? 'text-red-800' : alert.severity === 'warning' ? 'text-amber-800' : 'text-blue-800'}`}>
                  {alert.message}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Row 4: My Courses Grid */}
      <div className="glass-card p-6 rounded-3xl">
        <h3 className="text-lg font-semibold text-primary mb-4">My Courses 📚</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {courses?.map((course, i) => (
            <div key={i} className="bg-white/70 border border-white p-4 rounded-2xl flex flex-col hover:shadow-md transition">
              <div className="text-xs font-bold text-sky-600 mb-1">{course.code}</div>
              <div className="font-bold text-slate-800 text-sm mb-1">{course.name}</div>
              <div className="text-xs text-slate-500 font-semibold mb-4">Section: {course.section}</div>
              
              <div className="grid grid-cols-3 gap-2 mt-auto mb-4 text-center">
                <div className="bg-slate-50 rounded-lg p-1">
                  <div className="text-[10px] text-slate-400">Students</div>
                  <div className="font-bold text-slate-700 text-sm">{course.students}</div>
                </div>
                <div className="bg-slate-50 rounded-lg p-1">
                  <div className="text-[10px] text-slate-400">Att %</div>
                  <div className="font-bold text-slate-700 text-sm">{course.attendance}</div>
                </div>
                <div className="bg-slate-50 rounded-lg p-1">
                  <div className="text-[10px] text-slate-400">Avg %</div>
                  <div className="font-bold text-slate-700 text-sm">{course.avg_marks}</div>
                </div>
              </div>
              <button className="w-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold py-2 rounded-xl transition flex justify-center items-center gap-1">
                Open Course <ChevronRight size={12}/>
              </button>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}

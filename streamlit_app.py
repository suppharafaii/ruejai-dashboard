import streamlit as st
import google.generativeai as genai

# ส่วนเชื่อมต่อกับรหัสลับที่เราจะไปตั้งใน Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.title("📊 Ruejai Project Dashboard")

# ก๊อปปี้ข้อมูลที่คุณพิมพ์ไว้ใน AI Studio มาวางในนี้ครับ
SYSTEM_PROMPT = """
import reflex as rx
from typing import List, Dict, Optional

# --- Data Models ---
class Milestone(rx.Base):
    label: str
    date_range: str

class Project(rx.Base):
    id: str
    title: str
    target_date: str
    milestones: List[Milestone]
    current_status: str
    readiness_score: int
    theme: str # 'green', 'blue', 'purple', 'orange', 'yellow', 'slate', 'pink'
    dev_team: str # 'TS' or 'CodeApp'

# --- Application State ---
class State(rx.State):
    projects: List[Project] = [
        Project(
            id="1", title="Revamp Profile Widget", target_date="5 Feb'26",
            theme="green", current_status="Status: Go Live", readiness_score=100, dev_team="TS",
            milestones=[Milestone(label="Design:", date_range="5 Jan'26 → 15 Jan'26 (Finished)")]
        ),
        # ... เพิ่มโปรเจคอื่นๆ ตาม constants.tsx
    ]
    team_filter: str = "All"

    @rx.var
    def filtered_projects(self) -> List[Project]:
        if self.team_filter == "All":
            return self.projects
        return [p for p in self.projects if p.dev_team == self.team_filter]

# --- UI Components ---

def project_card(project: Project):
    # Mapping themes to tailwind classes
    theme_map = {
        "green": "bg-emerald-500",
        "blue": "bg-blue-500",
        "purple": "bg-purple-500",
        "orange": "bg-orange-400",
        "yellow": "bg-amber-300",
        "slate": "bg-slate-400",
        "pink": "bg-pink-500",
    }
    header_color = theme_map.get(project.theme, "bg-slate-400")

    return rx.box(
        # Header Cap
        rx.box(class_name=f"h-2.5 w-full {header_color}"),
        
        rx.vstack(
            # Title & Team
            rx.hstack(
                rx.vstack(
                    rx.badge(f"TEAM: {project.dev_team}", variant="subtle", color_scheme="indigo"),
                    rx.heading(project.title, size="4", class_name="uppercase font-bold text-slate-800"),
                    align_items="start",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("Target Date", class_name="text-[8px] font-bold text-slate-300 uppercase"),
                    rx.box(
                        rx.text(project.target_date, class_name="text-red-500 font-bold italic"),
                        class_name="px-3 py-1 border border-red-50 rounded-lg bg-white"
                    ),
                    align_items="end",
                ),
                width="100%",
            ),

            # Milestones
            rx.vstack(
                rx.hstack(
                    rx.box(class_name="w-1 h-3 bg-slate-800 rounded-full"),
                    rx.text("Operational Gates", class_name="text-[9px] font-bold uppercase tracking-widest"),
                ),
                rx.vstack(
                    *[rx.hstack(
                        rx.text(m.label, class_name="w-24 font-semibold text-slate-400 text-sm"),
                        rx.text(m.date_range, class_name="font-bold text-sm text-slate-700"),
                    ) for m in project.milestones],
                    spacing="1",
                ),
                align_items="start",
                width="100%",
                margin_top="4",
            ),

            # Status
            rx.box(
                rx.hstack(
                    rx.box(class_name="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"),
                    rx.text(project.current_status, class_name="text-[11px] font-bold text-slate-600"),
                ),
                class_name="bg-slate-50 px-4 py-2 rounded-xl mt-4 w-fit"
            ),

            rx.spacer(),

            # Readiness Score
            rx.hstack(
                rx.vstack(
                    rx.text("Readiness Score", class_name="text-[8px] font-bold text-slate-300 uppercase"),
                    rx.hstack(
                        rx.heading(str(project.readiness_score), size="8", class_name="font-black text-slate-800"),
                        rx.text("%", class_name="text-sm font-bold text-slate-300"),
                        align_items="baseline",
                    ),
                    align_items="start",
                ),
                rx.spacer(),
                rx.cond(
                    project.readiness_score == 100,
                    rx.badge("Launched", color_scheme="green", variant="solid")
                ),
                width="100%",
                padding_top="4",
                border_top="1px solid #f8fafc",
            ),
            
            padding="2rem",
            height="100%",
        ),
        
        # Progress Bar
        rx.box(
            rx.box(
                class_name=f"h-full {header_color}",
                style={"width": f"{project.readiness_score}%"}
            ),
            class_name="h-1 w-full bg-slate-50"
        ),

        class_name="bg-white rounded-[2rem] shadow-sm overflow-hidden border border-slate-100 flex flex-col h-full hover:shadow-lg transition-all",
    )

def index():
    return rx.box(
        # Header
        rx.box(
            rx.vstack(
                rx.badge("Strategic Assets 2026", variant="solid", class_name="bg-slate-900 text-white"),
                rx.heading("Ruejai Product Roadmap", size="9", class_name="font-bold text-slate-900"),
                rx.text("Executive Oversight Dashboard", class_name="text-slate-400 font-bold uppercase tracking-widest text-xs"),
                
                # Filter
                rx.hstack(
                    rx.text("Dev Team:", class_name="text-[10px] font-black text-slate-300 uppercase"),
                    rx.button_group(
                        rx.button("All", on_click=lambda: State.set_team_filter("All")),
                        rx.button("TS", on_click=lambda: State.set_team_filter("TS")),
                        rx.button("CodeApp", on_click=lambda: State.set_team_filter("CodeApp")),
                    ),
                    margin_top="4",
                ),
                align_items="start",
                max_width="1280px",
                margin="0 auto",
                padding="2rem",
            ),
            background="white",
            border_bottom="1px solid #e2e8f0",
        ),

        # Main Dashboard
        rx.box(
            rx.grid(
                rx.foreach(
                    State.filtered_projects,
                    project_card
                ),
                columns=[1, 2, 3],
                spacing="8",
                max_width="1280px",
                margin="4rem auto",
                padding="0 2rem",
            ),
            background="#f8fafc",
            min_height="100vh",
        )
    )

app = rx.App()
app.add_page(index)
"""

if st.button("สรุปรายงานสำหรับผู้บริหาร"):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(SYSTEM_PROMPT + "\nช่วยสรุป Progress งานเป็นข้อๆ")
    st.markdown(response.text)

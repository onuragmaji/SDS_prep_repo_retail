import streamlit as st

from content.sql_pandas_prep import PANDAS_TOPICS, SQL_TOPICS

st.set_page_config(page_title="SQL & Pandas Prep", page_icon=":material/database:", layout="wide")

st.title("SQL & Pandas interview prep")
st.caption("Senior Data Scientist: step-wise topics, examples, interviewer questions and LeetCode practice")

st.info(
    """
Work through each track in order. Every step has the concepts to know, a worked example,
questions seniors are typically asked, and LeetCode problems (number + link) to practice.
Tick problems as you solve them; progress lasts for this browser session.
LeetCode **Premium** problems are marked with a lock.
"""
)

DIFFICULTY_COLOR = {"Easy": "green", "Medium": "orange", "Hard": "red"}


def _key(track, topic, problem):
    return f"solved_{track}_{topic['step']}_{problem['number']}"


def _progress(track, topics):
    keys = [_key(track, t, p) for t in topics for p in t["problems"]]
    done = sum(1 for k in keys if st.session_state.get(k, False))
    return done, len(keys)


def _render_track(track, topics):
    done, total = _progress(track, topics)
    st.progress(done / total if total else 0.0, text=f"Solved {done} of {total} problems")

    levels = st.pills(
        "Show difficulty",
        options=["Easy", "Medium", "Hard"],
        selection_mode="multi",
        default=["Easy", "Medium", "Hard"],
        key=f"levels_{track}",
    )

    for topic in topics:
        t_done = sum(1 for p in topic["problems"] if st.session_state.get(_key(track, topic, p), False))
        suffix = f"  ({t_done}/{len(topic['problems'])})" if topic["problems"] else ""
        with st.expander(f"Step {topic['step']}: {topic['title']}{suffix}"):
            st.markdown(f"**Why it matters:** {topic['why']}")

            st.markdown("**Concepts**")
            st.markdown("\n".join(f"- {c}" for c in topic["concepts"]))

            ex = topic["example"]
            st.markdown("**Example**")
            st.code(ex["code"], language=ex["language"])
            st.caption(ex["note"])

            st.markdown("**Questions to expect**")
            st.markdown("\n".join(f"- {q}" for q in topic["questions"]))

            if topic["problems"]:
                st.markdown("**Practice on LeetCode**")
                for p in topic["problems"]:
                    if p["difficulty"] not in (levels or []):
                        continue
                    c_check, c_title, c_diff = st.columns([1, 8, 2], vertical_alignment="center")
                    c_check.checkbox(
                        f"Solved {p['number']}",
                        key=_key(track, topic, p),
                        label_visibility="collapsed",
                    )
                    lock = " :material/lock:" if p["premium"] else ""
                    c_title.markdown(f"[{p['number']}. {p['title']}]({p['url']}){lock}")
                    c_diff.markdown(f":{DIFFICULTY_COLOR[p['difficulty']]}[{p['difficulty']}]")
            else:
                st.caption("Discussion / case topic: no LeetCode problems.")


tab_sql, tab_pandas = st.tabs([":material/database: SQL", ":material/table: Pandas"])

with tab_sql:
    st.markdown(
        "Dialect note: examples use MySQL/PostgreSQL-style syntax, matching LeetCode. "
        "In an interview, say which dialect you assume."
    )
    _render_track("sql", SQL_TOPICS)

with tab_pandas:
    st.markdown(
        "LeetCode's *30 Days of Pandas* set covers the basics (2877-2891). Many classic SQL problems "
        "can also be solved in pandas by switching the language on the problem page, which is "
        "the best practice for steps 4, 5, 7 and 8."
    )
    _render_track("pandas", PANDAS_TOPICS)

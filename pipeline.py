import time
from langgraph.errors import GraphRecursionError
from agents import build_search_agent, build_search_reader_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # step 1 - search agent
    print("\n" + "=" * 50)
    print("Step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]},
        config={"recursion_limit": 15},
    )
    state["search_results"] = search_result["messages"][-1].content

    print("\n search result", state["search_results"])

    time.sleep(10)  # TPM budget refill

    # step 2 - reader agent
    print("\n" + "=" * 50)
    print("step 2 - reader agent is scraping top resources...")
    print("=" * 50)

    reader_agent = build_search_reader_agent()
    try:
        reader_result = reader_agent.invoke(
            {"messages": [("user",
                f"Topic: '{topic}'\n\n"
                f"Search results:\n{state['search_results'][:2500]}\n\n"
                "Pick the SINGLE most relevant URL and call scrape_url exactly ONCE. "
                "Then summarize the content in under 200 words."
            )]},
            config={"recursion_limit": 15},
        )
        state["scrap_result"] = reader_result["messages"][-1].content
    except GraphRecursionError:
        state["scrap_result"] = "Reader agent could not finish scraping; using search results only."

    print("\n scraped content", state["scrap_result"])

    time.sleep(10)

    # step 3 - writer chain
    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report... ")
    print("=" * 50)

    research_combine = (
        f"Search results : \n {state['search_results'][:2500]}\n\n"
        f"Detailed scraped content : \n {state['scrap_result'][:2500]}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combine,
    })

    print("\n Report\n", state["report"])

    time.sleep(30)  # writer ke baad budget refill, critic se pehle

    # step 4 - critic
    print("\n" + "=" * 50)
    print("step 4 - critic is reviewing the report")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    print("\n Feedback ", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("Enter research topic: ")
    result = run_research_pipeline(topic)
    print(result)
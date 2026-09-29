import time  # ADDED
from agents import build_search_agent, build_search_reader_agent, writer_chain, critic_chain  # CHANGED: spelling fix


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # step 1 - search agent
    print("\n" + "=" * 50)
    print("Step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()  # CHANGED
    search_result = search_agent.invoke(
        {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]},
        config={"recursion_limit": 6},  # ADDED: agent loop cap
    )
    state["search_results"] = search_result["messages"][-1].content

    print("\n search result", state["search_results"])

    time.sleep(10)  # ADDED: TPM budget refill

    # step 2 - reader agent
    print("\n" + "=" * 50)
    print("step 2 - reader agent is scraping top resources...")
    print("=" * 50)

    reader_agent = build_search_reader_agent()
    reader_result = reader_agent.invoke(
        {"messages": [("user",
            f"Topic: '{topic}'\n\n"
            f"Search results:\n{state['search_results'][:2500]}\n\n"  # CHANGED: 800 -> 2500 (URLs cut na hon)
            "Pick the SINGLE most relevant URL and call scrape_url exactly ONCE. "  # CHANGED
            "Then summarize the content in under 200 words."
        )]},
        config={"recursion_limit": 6},  # ADDED
    )

    state["scrap_result"] = reader_result["messages"][-1].content
    print("\n scraped content", state["scrap_result"])

    time.sleep(10)  # ADDED

    # step 3 - writer chain
    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report... ")
    print("=" * 50)

    research_combine = (
        f"Search results : \n {state['search_results'][:2500]}\n\n"  # CHANGED: cap
        f"Detailed scraped content : \n {state['scrap_result'][:2500]}"  # CHANGED: cap
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combine,
    })

    print("\n Report\n", state["report"])

    time.sleep(30)  # ADDED: writer ne 120b ka budget kharch kiya, critic se pehle refill

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
from agents import build_serach_agent,build_search_reader_agent,writer_chain,critic_chain

def run_research_pipeline(topic:str)->dict:
    state = {}
    
    #search agent working
    print("\n"+"="*50)
    print("Step 1 - search agent is working ...")
    print("="*50)
    
    search_agent = build_serach_agent()
    search_result=search_agent.invoke({
        "messages":[('user',f"Find recent , reliable and detailed information about: {topic}")]
    })
    state['search_results']=search_result['messages'][-1].content
    
    print("\n search result",state['search_results'])
    
    #step 2- reader agent
    print("\n"+"="*50)
    print("step 2 - reader agent is scraping top resources...")
    print("="*50)
    
    reader_agent=build_search_reader_agent()
    reader_result=reader_agent.invoke({
        "messages":[("user",
                     f"Based  on the following  result about '{topic}',"
                     f"pick the most relevant URL and scrape it for deeper content.\n\n"
                     f"Search Result:\n{state['search_results'][:800]}"
                     )]
    })
    
    state['scrap_result']=reader_result['messages'][-1].content
    print("\n scraped content",state['scrap_result'])
    
    #step 3: writer chain
    print("\n"+"="*50)
    print("Step 3 - Writer is drafting the report... ")
    print("="*50)
    
    research_combine=(
        f"Search results : \n {state['search_results']}\n\n"
        f"Detailed scraped content : \n {state['scrap_result']}"
    )
    
    state['report']=writer_chain.invoke({
        "topic":topic,
        "research":research_combine
    })
    
    print("\n Report\n",state['report'])
    
    # step 4 - critic report
    print("\n"+"="*50)
    print("step 4 - critic is reviewing the report")
    print("="*50)

    state['feedback']=critic_chain.invoke({"report":state['report']})
    
    print("\n Feedback ",state['feedback'])
    
    return state

if __name__ == "__main__":
    topic = input("Enter research topic: ")
    result = run_research_pipeline(topic)
    print(result)
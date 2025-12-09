"""
Pharmaceutical Multi-Agent Research System using CrewAI Framework
Integrates with Ollama LLM for agent intelligence
"""

from crewai import Agent, Task, Crew, Process,LLM
from crewai_tools import SerperDevTool, FileReadTool, ScrapeWebsiteTool
from langchain_ollama import OllamaLLM
import os
import sys
from datetime import datetime


llm = LLM(
    model="ollama/llama3:latest",          
    base_url="http://localhost:11434",
    temperature=0.0                 
)


# Initialize tools (only those that don't require API keys for basic demo)
# For production, add: export SERPER_API_KEY="your_key"
search_tool = SerperDevTool() if os.getenv("SERPER_API_KEY") else None
# file_tool = FileReadTool()
scrape_tool = ScrapeWebsiteTool()


# ============================================================================
# WORKER AGENTS DEFINITION
# ============================================================================

# 1. IQVIA Insights Agent
iqvia_agent = Agent(
    role='IQVIA Market Intelligence Analyst',
    goal='Analyze pharmaceutical market data, sales trends, volume shifts, and therapy area dynamics',
    backstory="""You are an expert market analyst specializing in pharmaceutical 
    market intelligence. You have deep expertise in analyzing IQVIA datasets, 
    understanding market size, CAGR trends, and competitive therapy-level dynamics. 
    You provide data-driven insights on sales performance and market opportunities.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool] if search_tool else []
)

# 2. EXIM Trends Agent
exim_agent = Agent(
    role='Export-Import Trade Analyst',
    goal='Extract and analyze export-import data for APIs and formulations across countries',
    backstory="""You are a trade analyst specializing in pharmaceutical supply chains. 
    You excel at tracking international trade flows, identifying sourcing patterns, 
    and analyzing import dependencies. You provide insights on trade volumes, 
    country-wise sourcing, and supply chain dynamics.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool] if search_tool else []
)

# 3. Patent Landscape Agent
patent_agent = Agent(
    role='Intellectual Property Research Specialist',
    goal='Search and analyze patent databases for active patents, expiry timelines, and freedom-to-operate analysis',
    backstory="""You are an IP research expert with deep knowledge of patent databases 
    including USPTO, EPO, and WIPO. You analyze patent landscapes, identify competitive 
    filings, assess patent expiry timelines, and provide FTO (Freedom to Operate) insights. 
    You help identify white spaces for innovation.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool, scrape_tool] if search_tool else [scrape_tool]
)

# 4. Clinical Trials Agent
clinical_trials_agent = Agent(
    role='Clinical Trials Research Analyst',
    goal='Fetch and analyze clinical trial pipeline data from ClinicalTrials.gov and WHO ICTRP',
    backstory="""You are a clinical research analyst specializing in trial pipeline analysis. 
    You track ongoing and completed clinical trials, analyze sponsor profiles, study phase 
    distributions, and identify emerging therapeutic approaches. You provide comprehensive 
    insights into the clinical development landscape.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool, scrape_tool] if search_tool else [scrape_tool]
)

# 5. Internal Knowledge Agent
internal_knowledge_agent = Agent(
    role='Internal Knowledge Manager',
    goal='Retrieve and summarize internal documents including strategy decks, meeting minutes, and field insights',
    backstory="""You are an internal knowledge expert who maintains and analyzes the 
    company's institutional knowledge. You excel at retrieving relevant internal documents, 
    extracting key insights, and creating comparative analyses from internal data sources. 
    You bridge the gap between historical knowledge and current research needs.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[]   #[file_tool]
)

# 6. Web Intelligence Agent
web_intelligence_agent = Agent(
    role='Web Intelligence Researcher',
    goal='Perform real-time web searches for clinical guidelines, scientific publications, news, and patient forums',
    backstory="""You are a web research specialist with expertise in finding and synthesizing 
    information from diverse online sources. You excel at identifying credible sources, 
    extracting relevant guidelines, summarizing scientific publications, and tracking 
    real-world evidence from patient communities and medical news.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[search_tool, scrape_tool] if search_tool else [scrape_tool]
)

# 7. Report Generator Agent
report_generator_agent = Agent(
    role='Research Report Compiler',
    goal='Synthesize all research findings into polished, comprehensive reports with visualizations',
    backstory="""You are a scientific writer and data visualization expert. You excel at 
    taking complex research findings from multiple sources and creating clear, comprehensive 
    reports. You organize information logically, create insightful tables and charts, and 
    present findings in formats suitable for executive decision-making.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# 8. Master Agent (Orchestrator)
master_agent = Agent(
    role='Research Orchestrator and Strategy Lead',
    goal='Interpret user queries, delegate tasks to specialized agents, and synthesize comprehensive insights',
    backstory="""You are the chief research strategist who understands the complete 
    pharmaceutical innovation lifecycle. You break down complex research questions into 
    specific tasks, delegate to domain experts, and synthesize their findings into 
    actionable intelligence. You ensure all aspects of a research question are thoroughly 
    investigated.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)


# ============================================================================
# TASK CREATION FUNCTIONS
# ============================================================================

def create_market_analysis_task(molecule_name):
    """Create task for IQVIA market analysis"""
    return Task(
        description=f"""Analyze the market landscape for {molecule_name}:
        1. Current market size and growth trends (CAGR)
        2. Major therapy areas and indications
        3. Competitive landscape and key players
        4. Sales volume trends and market dynamics
        5. Pricing patterns and reimbursement landscape
        
        Provide specific data points, market sizes in USD, and growth percentages.
        If you don't have access to real-time data, provide a structured analysis 
        framework and known information about this molecule.""",
        agent=iqvia_agent,
        expected_output="Detailed market analysis with tables showing market size, CAGR, and competitive positioning"
    )

def create_trade_analysis_task(molecule_name):
    """Create task for EXIM trade analysis"""
    return Task(
        description=f"""Analyze export-import dynamics for {molecule_name} and its API:
        1. Major exporting and importing countries
        2. Trade volumes and value trends (last 3 years)
        3. Key manufacturing hubs and sourcing patterns
        4. Import dependency analysis for major markets
        5. Regulatory considerations for cross-border trade
        
        Focus on API and finished formulation trade data. Provide insights based on 
        known pharmaceutical trade patterns and this molecule's characteristics.""",
        agent=exim_agent,
        expected_output="Trade analysis report with country-wise import/export data and sourcing insights"
    )

def create_patent_analysis_task(molecule_name):
    """Create task for patent landscape analysis"""
    return Task(
        description=f"""Conduct comprehensive patent analysis for {molecule_name}:
        1. Active patents (composition, formulation, use patents)
        2. Patent expiry timelines (provide specific dates if known)
        3. Key patent holders and their filing strategies
        4. Freedom-to-operate assessment for new indications/formulations
        5. Patent landscape showing competitive intensity
        
        You can scrape https://patents.google.com or use your knowledge of patent 
        databases to provide insights. Focus on USPTO and major patent offices.""",
        agent=patent_agent,
        expected_output="Patent landscape report with expiry dates, FTO analysis, and competitive filing patterns"
    )

def create_clinical_trials_task(molecule_name):
    """Create task for clinical trials research"""
    return Task(
        description=f"""Research clinical trial landscape for {molecule_name}:
        1. Active clinical trials across all phases
        2. Completed trials with outcomes
        3. New indications being investigated
        4. Sponsor profiles (pharma companies, academic institutions)
        5. Trial design trends and patient populations
        6. Emerging therapeutic uses beyond approved indications
        
        You can scrape ClinicalTrials.gov (https://clinicaltrials.gov) or provide 
        analysis based on known clinical development patterns for this molecule.""",
        agent=clinical_trials_agent,
        expected_output="Clinical trials analysis with trial counts by phase, sponsors, and novel indications"
    )

def create_internal_knowledge_task(molecule_name):
    """Create task for internal knowledge retrieval"""
    return Task(
        description=f"""Retrieve and synthesize internal company knowledge about {molecule_name}:
        1. Previous research and strategy documents
        2. Field insights from medical teams
        3. Historical development attempts or considerations
        4. Internal market assessments
        5. Competitive intelligence reports
        
        If no internal documents are available, provide a framework for what internal 
        knowledge should be collected about this molecule.""",
        agent=internal_knowledge_agent,
        expected_output="Summary of internal knowledge with key strategic insights and historical context"
    )

def create_web_intelligence_task(molecule_name):
    """Create task for web intelligence gathering"""
    return Task(
        description=f"""Gather comprehensive web intelligence on {molecule_name}:
        1. Clinical practice guidelines mentioning the molecule
        2. Recent scientific publications and breakthrough research
        3. Medical news and developments
        4. Patient perspectives and real-world experiences
        5. Unmet medical needs in current indication areas
        6. Potential new therapeutic applications based on mechanism of action
        
        Focus on credible medical sources, peer-reviewed journals, and official 
        clinical guidelines. Provide URLs when possible.""",
        agent=web_intelligence_agent,
        expected_output="Web intelligence report with sources, key publications, and unmet needs analysis"
    )

def create_report_generation_task():
    """Create task for final report compilation"""
    return Task(
        description="""Compile all research findings into a comprehensive innovation opportunity report:
        
        Structure the report as follows:
        
        1. EXECUTIVE SUMMARY
           - Key findings in 3-5 bullet points
           - Top innovation opportunities
           - Critical recommendations
        
        2. MOLECULE OVERVIEW
           - Mechanism of action
           - Current approved indications
           - Pharmacological properties
        
        3. MARKET ANALYSIS
           - Market size and growth (CAGR)
           - Competitive landscape
           - Key market players
           - Pricing and reimbursement
        
        4. PATENT LANDSCAPE
           - Active patents and expiry dates
           - Freedom-to-operate assessment
           - White space opportunities
        
        5. CLINICAL DEVELOPMENT PIPELINE
           - Ongoing trials by phase
           - Emerging indications
           - Sponsor analysis
        
        6. TRADE AND SUPPLY CHAIN
           - Manufacturing locations
           - Import/export dynamics
           - Supply chain risks
        
        7. UNMET MEDICAL NEEDS
           - Current treatment gaps
           - Patient pain points
           - Market opportunities
        
        8. INNOVATION OPPORTUNITIES (PRIORITIZED)
           - New indications
           - Alternative formulations
           - Different patient populations
           - Each with: rationale, feasibility, market potential
        
        9. RISK ASSESSMENT
           - Technical risks
           - Regulatory risks
           - Commercial risks
        
        10. RECOMMENDATIONS AND NEXT STEPS
            - Top 3 opportunities to pursue
            - Suggested timeline
            - Required resources
        
        Format with clear headers, bullet points, and tables where appropriate.
        Make it executive-ready and actionable.""",
        agent=report_generator_agent,
        expected_output="Comprehensive innovation research report with executive summary, detailed analysis, and prioritized recommendations"
    )


# ============================================================================
# CREW ORCHESTRATION
# ============================================================================

def create_pharma_research_crew(molecule_name, research_focus=None):
    """
    Create and configure the pharmaceutical research crew
    
    Args:
        molecule_name: Name of the molecule to research
        research_focus: Optional specific focus areas
    """
    
    # Create all research tasks
    tasks = [
        create_market_analysis_task(molecule_name),
        create_trade_analysis_task(molecule_name),
        create_patent_analysis_task(molecule_name),
        create_clinical_trials_task(molecule_name),
        create_internal_knowledge_task(molecule_name),
        create_web_intelligence_task(molecule_name),
        create_report_generation_task()
    ]
    
    # Create the crew with sequential process
    crew = Crew(
        agents=[
            iqvia_agent,
            exim_agent,
            patent_agent,
            clinical_trials_agent,
            internal_knowledge_agent,
            web_intelligence_agent,
            report_generator_agent
        ],
        tasks=tasks,
        process=Process.sequential,  # Tasks execute in order
        verbose=True
    )
    
    return crew


# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

def run_pharmaceutical_research(molecule_name, save_report=True):
    """
    Execute the complete pharmaceutical research workflow
    
    Args:
        molecule_name: Name of the molecule to research
        save_report: Whether to save the report to file
    
    Returns:
        Research results and report
    """
    
    print(f"\n{'='*80}")
    print(f"PHARMACEUTICAL INNOVATION RESEARCH SYSTEM")
    print(f"Molecule: {molecule_name}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    # Check if Serper API key is set
    if not os.getenv("SERPER_API_KEY"):
        print("⚠️  WARNING: SERPER_API_KEY not set. Web search capabilities will be limited.")
        print("   Set it with: export SERPER_API_KEY='your_key'")
        print("   Get your key from: https://serper.dev\n")
    
    # Create the research crew
    crew = create_pharma_research_crew(molecule_name)
    
    # Execute the research
    print("🚀 Initiating multi-agent research workflow...\n")
    
    try:
        result = crew.kickoff()
        
        # Always save to output.txt for API consumption
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, 'output.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(result))
        print(f"\n📄 Output saved to: {output_file}")
        
        # Also save timestamped report if requested
        if save_report:
            report_filename = os.path.join(
                script_dir,
                f"pharma_research_{molecule_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(str(result))
            print(f"📄 Report saved to: {report_filename}")
        
        print(f"\n{'='*80}")
        print("✅ RESEARCH COMPLETE")
        print(f"{'='*80}\n")
        
        return result
    
    except Exception as e:
        print(f"\n❌ Error during research: {str(e)}")
        
        # Write error to output.txt
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, 'output.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Research Error\n\nAn error occurred during research: {str(e)}")
        
        return None


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Get molecule name from command line or environment
    if len(sys.argv) > 1:
        molecule = sys.argv[1]
    elif os.getenv('MOLECULE_NAME'):
        molecule = os.getenv('MOLECULE_NAME')
    else:
        molecule = "Metformin"
    
    print("Starting pharmaceutical research for:", molecule)
    print("This will take several minutes as agents work through their tasks...\n")
    
    result = run_pharmaceutical_research(molecule)
    
    if result:
        print("\n" + "="*80)
        print("FINAL RESEARCH REPORT")
        print("="*80)
        print(result)

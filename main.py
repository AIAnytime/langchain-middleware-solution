"""
LangChain v1.0 Middleware Solution - Main Entry Point

This demo showcases the middleware architecture introduced in LangChain v1.0
for systematic AI agent context control.
"""

from demo_examples import main as run_demos


def main():
    """Main entry point for the middleware demonstration"""
    print("\nLangChain v1.0 Middleware Solution")
    print("Systematic Context Control for AI Agents\n")
    
    try:
        run_demos()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please ensure your .env file contains valid API keys.")


if __name__ == "__main__":
    main()

import os
import sys

# Ensure backend dir is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from porownanie.protocol_orchestrator import ProtocolOrchestrator

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")

    orchestrator = ProtocolOrchestrator(input_dir, output_dir)
    orchestrator.generate_protocol()

if __name__ == "__main__":
    main()

import torch
import torch.nn as nn
import torch.optim as optim

def check_mps_availability():
    print("\n=== MPS Availability Check ===")
    
    if not torch.backends.mps.is_available():
        if not torch.backends.mps.is_built():
            print("❌ MPS not available because the current PyTorch install was not "
                  "built with MPS enabled.")
        else:
            print("❌ MPS not available because the current MacOS version is not 12.3+ "
                  "and/or you do not have an MPS-enabled device on this machine.")
        return False
    
    print("✅ MPS is available!")
    return True

def demonstrate_mps():
    print("\n=== MPS Demonstration ===")
    
    # Set up MPS device
    mps_device = torch.device("mps")
    print(f"Using device: {mps_device}")
    
    # Create a tensor on MPS device
    print("\nCreating tensor on MPS device...")
    x = torch.ones(5, device=mps_device)
    print(f"Tensor x: {x}")
    
    # Perform basic operation
    print("\nPerforming basic operation (multiply by 2)...")
    y = x * 2
    print(f"Result y (x * 2): {y}")
    
    # Define a simple neural network
    class SimpleNet(nn.Module):
        def __init__(self):
            super(SimpleNet, self).__init__()
            self.layer = nn.Linear(5, 1)
            
        def forward(self, x):
            return self.layer(x)
    
    # Create and move model to MPS
    print("\nCreating and moving model to MPS...")
    model = SimpleNet()
    model.to(mps_device)
    
    # Run inference
    print("Running inference...")
    with torch.no_grad():
        pred = model(x)
    print(f"Model prediction: {pred}")

def main():
    print("🔍 Checking MPS (Metal Performance Shaders) on your system...")
    
    if check_mps_availability():
        try:
            demonstrate_mps()
            print("\n✨ MPS demonstration completed successfully!")
        except Exception as e:
            print(f"\n❌ Error during MPS demonstration: {str(e)}")
    else:
        print("\n⚠️ Skipping MPS demonstration since MPS is not available.")

if __name__ == "__main__":
    main()

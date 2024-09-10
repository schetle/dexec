import subprocess
import time
import click

# Function to run a command and capture its execution time in milliseconds
def run_command_and_time(cmd):
    start_time = time.time()  # Start time
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end_time = time.time()  # End time
    elapsed_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
    return elapsed_time_ms

# Function to benchmark a single command
def benchmark_command(command, iterations):
    total_time = 0

    # Run the command for the specified number of iterations
    for _ in range(iterations):
        exec_time = run_command_and_time(command)
        total_time += exec_time

    # Calculate the average time
    average_time = total_time / iterations
    return average_time

# Click interface for command-line usage
@click.command()
@click.option('-c1', '--command1', required=True, help='First command to benchmark (e.g., python main.py)')
@click.option('-c2', '--command2', required=True, help='Second command to benchmark (e.g., docker exec)')
@click.option('-i', '--iterations', default=100, help='Number of iterations to run each command (default is 100)')
def main(command1, command2, iterations):
    """
    This script benchmarks two commands (COMMAND1 and COMMAND2) for a specified number of ITERATIONS.
    """

    # Benchmark the first command
    click.echo(f"Benchmarking '{command1}' for {iterations} iterations...")
    avg_time_command1 = benchmark_command(command1, iterations)
    click.echo(f"Average time for '{command1}': {avg_time_command1:.3f} milliseconds over {iterations} iterations\n")

    # Benchmark the second command
    click.echo(f"Benchmarking '{command2}' for {iterations} iterations...")
    avg_time_command2 = benchmark_command(command2, iterations)
    click.echo(f"Average time for '{command2}': {avg_time_command2:.3f} milliseconds over {iterations} iterations\n")

    # Print the results side by side for comparison
    click.echo(f"Comparison:")
    click.echo(f"  {command1}: {avg_time_command1:.3f} ms")
    click.echo(f"  {command2}: {avg_time_command2:.3f} ms")

# Entry point
if __name__ == "__main__":
    main()

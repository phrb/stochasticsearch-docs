@everywhere begin
    using StochasticSearch
    function tour_cost(x::Configuration, parameters::Dict{Symbol, Any})
        result = float(readall(`./tour_cost $(x["Tour"].value)`))
        result
    end
end

println("[Starting Tuning Experiment]")

target   = "results/att532"
size     = 532
runs     = 6
duration = 600

run(`mkdir $target`)
run(`mkdir $target/jl`)

for j = 1:runs
    println("[Initializing Tuning Run $(string(j))]")
    tour = ["1"]
    for i = 2:size
        push!(tour, string(i))
    end
    shuffle!(tour)

    configuration = Configuration([PermutationParameter(tour ,"Tour")],
                                   "TSP Solution")

    methods     = [:iterative_first_improvement,
                   :iterative_greedy_construction,
                   :iterative_probabilistic_improvement,
                   :randomized_first_improvement,
                   :simulated_annealing]

    instances   = [2, 2, 2, 2, 2]

    parameters = Dict(:cost               => tour_cost,
                      :cost_args          => Dict{Symbol, Any}(),
                      :initial_config     => configuration,
                      :report_after       => 20,
                      :measurement_method => sequential_measure_mean!,
                      :stopping_criterion => elapsed_time_criterion,
                      :seconds            => duration,
                      :methods            => methods,
                      :instances          => instances,
                      :evaluations        => 1)

    search_task = @task optimize(parameters)

    run(`mkdir $target/jl/run_$(string(j))`)
    best = open("$target/jl/run_$(string(j))/best.txt", "a")
    last = open("$target/jl/run_$(string(j))/last.txt", "a")
    conf = open("$target/jl/run_$(string(j))/best_configuration.txt", "a")

    println("[Done]\n[Starting Run $(string(j))]")
    result = consume(search_task)
    println(best, "$(string(result.current_time)) $(string(result.cost_minimum))")
    print("[.")
    while result.is_final == false
        result = consume(search_task)
        println(best, "$(string(result.current_time)) $(string(result.cost_minimum))")
        print(".")
    end
    println(last, "$(string(result.current_time)) $(string(result.cost_minimum))")
    println(".]")
    println("[Saving Best Configuration]")
    for i in result.minimum["Tour"].value
        println(conf, i)
    end
    close(best)
    close(last)
    close(conf)
    println("[Run $(string(j)) is done]")
end

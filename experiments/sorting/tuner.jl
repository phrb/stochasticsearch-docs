@everywhere begin
    using StochasticSearch
    function sort(x::Configuration, parameters::Dict{Symbol, Any})
        cutoff = x.value["cutoff"]
        @elapsed run(`./sorting $(cutoff)`)
    end
end

println("[Starting Tuning Experiment]")

target   = "results/2_17/jl/15min/1w"
size     = 131072
max_cut  = 200
runs     = 4 
duration = 900

#run(`mkdir $target`)

for j = 1:runs
    println("[Initializing Tuning Run $(string(j))]")

    configuration = Configuration([IntegerParameter(1, max_cut, "cutoff")],
                                   "Sorting Cutoff")

    methods     = [:iterative_first_improvement,
                   :iterative_greedy_construction,
                   :iterative_probabilistic_improvement,
                   :randomized_first_improvement,
                   :simulated_annealing]

    instances   = [2, 2, 2, 2, 2]

    parameters = Dict(:cost               => sort,
                      :cost_args          => Dict{Symbol, Any}(),
                      :initial_config     => configuration,
                      :report_after       => 20,
                      :measurement_method => measure_mean!,
                      :stopping_criterion => elapsed_time_criterion,
                      :seconds            => duration,
                      :methods            => methods,
                      :instances          => instances,
                      :evaluations        => 4)

    search_task = @task optimize(parameters)

    run(`mkdir $target/run_$(string(j))`)
    best = open("$target/run_$(string(j))/best.txt", "a")
    last = open("$target/run_$(string(j))/last.txt", "a")
    conf = open("$target/run_$(string(j))/best_configuration.txt", "a")

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
    for i in result.minimum["cutoff"].value
        println(conf, i)
    end
    println(conf, result.minimum["cutoff"].value[1])

    close(best)
    close(last)
    close(conf)
    println("[Run $(string(j)) is done]")
end

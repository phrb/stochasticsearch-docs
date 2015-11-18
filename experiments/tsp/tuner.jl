@everywhere begin
    using StochasticSearch, Base.Random.uuid4
    function tour_cost(x::Configuration, parameters::Dict{Symbol, Any})
        filename   = ".tmp/$(string(uuid4()))"
        file       = open(filename, "w")
        round_trip = "$(join(x["Tour"].value, "\n"))\n$(x["Tour"].value[1])\n"
        write(file, round_trip)
        close(file)
        result     = float(readall(`./tour_cost $(filename)`))
        run(`rm $(filename)`)
        result
    end
end

println("[Starting Tuning Experiment]")

target   = "results/pla85900/jl/15min/1w_smm"
size     = 85900
runs     = 8
duration = 900

#run(`mkdir $target`)

run(`mkdir .tmp`)

for j = 5:runs
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
    for i in result.minimum["Tour"].value
        println(conf, i)
    end
    println(conf, result.minimum["Tour"].value[1])

    close(best)
    close(last)
    close(conf)
    println("[Run $(string(j)) is done]")
end

run(`rm -r .tmp`)

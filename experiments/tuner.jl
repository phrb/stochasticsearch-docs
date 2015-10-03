@everywhere begin
    using StochasticSearch
    function tour_cost(x::Configuration, parameters::Dict{Symbol, Any})
        result = float(readall(`./tour_cost $(x["Tour"].value)`))
        result
    end
end

tour = ["1"]
for i = 2:48
    push!(tour, string(i))
end
shuffle!(tour)

configuration = Configuration([PermutationParameter(tour ,"Tour")],
                               "TSP Solution")

methods     = [:simulated_annealing,
               :iterative_first_improvement,
               :randomized_first_improvement,
               :iterative_greedy_construction,
               :iterative_probabilistic_improvement]

instances   = [20, 20, 20, 20, 20]
iterations  = 100_000

parameters = Dict(:cost               => tour_cost,
                  :cost_args          => Dict{Symbol, Any}(),
                  :initial_config     => configuration,
                  :iterations         => iterations,
                  :report_after       => 200,
                  :cutoff             => 300,
                  :measurement_method => sequential_measure_mean!,
                  :stopping_criterion => elapsed_time_criterion,
                  :seconds            => 300,
                  :methods            => methods,
                  :instances          => instances,
                  :evaluations        => 1)

search_task = @task optimize(parameters)

result = consume(search_task)
print(result)
while result.is_final == false
    result = consume(search_task)
    print(result)
end

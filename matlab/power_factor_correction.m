clc;
clear;
close all;

%% ============================================================
%  INDUSTRIAL POWER MONITORING SYSTEM
%  Power Factor Correction Analysis
%
%  Assumption:
%  Capacitor bank is modeled using uniform 25-kVAR
%  switching steps.
%% ============================================================


%% ============================================================
%  1. SYSTEM PARAMETERS
%% ============================================================

P_total = 650;          % Total active power (kW)
Q_total = 380.122;      % Total reactive power (kVAR)

V = 415;                % LV line voltage (V)

transformer_rating = 1000;  % Transformer rating (kVA)

PF_target = 0.95;       % Desired target power factor

capacitor_step = 25;    % Capacitor switching step (kVAR)

max_bank_kvar = 500;    % Maximum available capacitor bank (kVAR)


%% ============================================================
%  2. ORIGINAL APPARENT POWER
%% ============================================================

S_original = sqrt( ...
    P_total^2 + Q_total^2);


%% ============================================================
%  3. ORIGINAL POWER FACTOR
%% ============================================================

PF_original = ...
    P_total / S_original;


%% ============================================================
%  4. CALCULATE INITIAL AND TARGET ANGLES
%% ============================================================

phi_initial = acos(PF_original);

phi_target = acos(PF_target);


%% ============================================================
%  5. THEORETICAL REQUIRED CAPACITOR kVAR
%% ============================================================

Q_required = ...
    P_total * ...
    (tan(phi_initial) - ...
     tan(phi_target));


%% ============================================================
%  6. SELECT SMALLEST PRACTICAL CAPACITOR BANK
%
%  The controller tests:
%
%  25, 50, 75, 100, 125, ...
%
%  and selects the smallest capacitor bank
%  that achieves the target PF.
%% ============================================================

Q_capacitor = NaN;

for Qc = capacitor_step:capacitor_step:max_bank_kvar

    % Reactive power after applying this capacitor
    Q_test = Q_total - Qc;

    % Apparent power after compensation
    S_test = sqrt( ...
        P_total^2 + Q_test^2);

    % Power factor after compensation
    PF_test = ...
        P_total / S_test;

    % Select the first capacitor size
    % that achieves the target PF
    if PF_test >= PF_target

        Q_capacitor = Qc;

        break;

    end

end


%% ============================================================
%  7. CHECK WHETHER TARGET PF IS ACHIEVABLE
%% ============================================================

if isnan(Q_capacitor)

    error( ...
        ['Target PF cannot be achieved with ' ...
         'the available capacitor bank.']);

end


%% ============================================================
%  8. CHECK MAXIMUM AVAILABLE CAPACITOR BANK
%% ============================================================

if Q_capacitor > max_bank_kvar

    error( ...
        ['Required capacitor bank exceeds ' ...
         'the maximum available capacity.']);

end


%% ============================================================
%  9. CALCULATE OVERCOMPENSATION
%% ============================================================

overcompensation = ...
    Q_capacitor - Q_required;


%% ============================================================
%  10. NEW REACTIVE POWER
%% ============================================================

Q_new = ...
    Q_total - Q_capacitor;


%% ============================================================
%  11. DETERMINE POWER FACTOR CONDITION
%% ============================================================

if Q_new > 0

    compensation_status = 'Lagging';

elseif Q_new < 0

    compensation_status = 'Leading';

else

    compensation_status = 'Unity PF';

end


%% ============================================================
%  12. NEW APPARENT POWER
%% ============================================================

S_new = sqrt( ...
    P_total^2 + Q_new^2);


%% ============================================================
%  13. ACTUAL ACHIEVED POWER FACTOR
%% ============================================================

PF_new = ...
    P_total / S_new;


%% ============================================================
%  14. TARGET PF CHECK
%% ============================================================

if PF_new >= PF_target

    PF_status = 'Target PF achieved';

else

    PF_status = 'Target PF not achieved';

end


%% ============================================================
%  15. CAPACITOR BANK UTILIZATION
%% ============================================================

capacitor_utilization = ...
    (Q_capacitor / max_bank_kvar) * 100;


%% ============================================================
%  16. CURRENT BEFORE PF CORRECTION
%% ============================================================

I_before = ...
    S_original * 1000 / ...
    (sqrt(3) * V);


%% ============================================================
%  17. CURRENT AFTER PF CORRECTION
%% ============================================================

I_after = ...
    S_new * 1000 / ...
    (sqrt(3) * V);


%% ============================================================
%  18. CURRENT REDUCTION
%% ============================================================

current_reduction = ...
    (I_before - I_after) ...
    / I_before * 100;


%% ============================================================
%  19. TRANSFORMER LOADING BEFORE CORRECTION
%% ============================================================

loading_before = ...
    S_original / ...
    transformer_rating * 100;


%% ============================================================
%  20. TRANSFORMER LOADING AFTER CORRECTION
%% ============================================================

loading_after = ...
    S_new / ...
    transformer_rating * 100;


%% ============================================================
%  21. DISPLAY RESULTS
%% ============================================================

fprintf('\n');
fprintf('=============================================\n');
fprintf('       POWER FACTOR CORRECTION ANALYSIS\n');
fprintf('=============================================\n');

fprintf('\n');

fprintf('Active Power                 : %.2f kW\n', ...
    P_total);

fprintf('Original Reactive Power     : %.2f kVAR\n', ...
    Q_total);

fprintf('Original Apparent Power     : %.2f kVA\n', ...
    S_original);

fprintf('Original Power Factor       : %.3f\n', ...
    PF_original);

fprintf('\n');

fprintf('Target Power Factor         : %.3f\n', ...
    PF_target);

fprintf('Required Capacitor          : %.2f kVAR\n', ...
    Q_required);

fprintf('Selected Practical Capacitor: %.2f kVAR\n', ...
    Q_capacitor);

fprintf('Overcompensation            : %.2f kVAR\n', ...
    overcompensation);

fprintf('\n');

fprintf('New Reactive Power          : %.2f kVAR\n', ...
    Q_new);

fprintf('New Apparent Power          : %.2f kVA\n', ...
    S_new);

fprintf('Actual Achieved PF          : %.3f\n', ...
    PF_new);

fprintf('Power Factor Condition      : %s\n', ...
    compensation_status);

fprintf('PF Status                   : %s\n', ...
    PF_status);

fprintf('Capacitor Bank Utilization  : %.2f %%\n', ...
    capacitor_utilization);

fprintf('\n');

fprintf('Current Before Correction   : %.2f A\n', ...
    I_before);

fprintf('Current After Correction    : %.2f A\n', ...
    I_after);

fprintf('Current Reduction           : %.2f %%\n', ...
    current_reduction);

fprintf('\n');

fprintf('Transformer Loading Before  : %.2f %%\n', ...
    loading_before);

fprintf('Transformer Loading After   : %.2f %%\n', ...
    loading_after);

fprintf('\n');
fprintf('=============================================\n');


%% ============================================================
%  22. FIGURE 1 - APPARENT POWER
%% ============================================================

figure;

values = [
    S_original
    S_new
];

bar(values);

xticklabels({
    'Before PF Correction'
    'After PF Correction'
});

ylabel('Apparent Power (kVA)');

title('Effect of Power Factor Correction on Apparent Power');

grid on;


%% ============================================================
%  23. FIGURE 2 - CURRENT
%% ============================================================

figure;

values = [
    I_before
    I_after
];

bar(values);

xticklabels({
    'Before PF Correction'
    'After PF Correction'
});

ylabel('Current (A)');

title('Effect of Power Factor Correction on LV Current');

grid on;


%% ============================================================
%  24. FIGURE 3 - TRANSFORMER LOADING
%% ============================================================

figure;

values = [
    loading_before
    loading_after
];

bar(values);

xticklabels({
    'Before PF Correction'
    'After PF Correction'
});

ylabel('Transformer Loading (%)');

title('Effect of PF Correction on Transformer Loading');

grid on;

hold on;

yline(100, '--', '100% Rating');

hold off;


%% ============================================================
%  25. FIGURE 4 - POWER FACTOR
%% ============================================================

figure;

values = [
    PF_original
    PF_new
];

bar(values);

xticklabels({
    'Before PF Correction'
    'After PF Correction'
});

ylabel('Power Factor');

title('Effect of Power Factor Correction on Power Factor');

ylim([0 1.05]);

grid on;

hold on;

yline(PF_target, '--', ...
    'Target PF');

hold off;

%% ============================================================
% SAVE PF CORRECTION RESULTS
% ============================================================

PF_condition = "Lagging";

if PF_new >= PF_target
    PF_status = "Target PF achieved";
else
    PF_status = "Target PF not achieved";
end

capacitor_utilization = ...
    (Q_capacitor / 500) * 100;

results_table = table( ...
    P_total, ...
    Q_total, ...
    S_original, ...
    PF_original, ...
    PF_target, ...
    Q_required, ...
    Q_capacitor, ...
    Q_capacitor - Q_required, ...
    Q_new, ...
    S_new, ...
    PF_new, ...
    I_before, ...
    I_after, ...
    current_reduction, ...
    loading_before, ...
    loading_after, ...
    capacitor_utilization, ...
    PF_condition, ...
    PF_status, ...
    'VariableNames', { ...
        'Active_Power_kW', ...
        'Original_Reactive_Power_kVAR', ...
        'Original_Apparent_Power_kVA', ...
        'Original_PF', ...
        'Target_PF', ...
        'Required_Capacitor_kVAR', ...
        'Selected_Capacitor_kVAR', ...
        'Overcompensation_kVAR', ...
        'New_Reactive_Power_kVAR', ...
        'New_Apparent_Power_kVA', ...
        'Achieved_PF', ...
        'Current_Before_A', ...
        'Current_After_A', ...
        'Current_Reduction_Percent', ...
        'Transformer_Loading_Before_Percent', ...
        'Transformer_Loading_After_Percent', ...
        'Capacitor_Bank_Utilization_Percent', ...
        'PF_Condition', ...
        'PF_Status' ...
    } ...
);

%% ------------------------------------------------------------
% Save CSV
% ------------------------------------------------------------

BASE_DIR = fileparts( ...
    fileparts( ...
        mfilename('fullpath') ...
    ) ...
);

OUTPUT_FILE = fullfile( ...
    BASE_DIR, ...
    'data', ...
    'pf_correction_results.csv' ...
);

writetable( ...
    results_table, ...
    OUTPUT_FILE ...
);

fprintf('\n');
fprintf('PF correction results saved to:\n');
fprintf('%s\n', OUTPUT_FILE);
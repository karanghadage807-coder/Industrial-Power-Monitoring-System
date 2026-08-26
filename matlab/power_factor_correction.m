clc;
clear;
close all;


%% System Parameters

P_total = 650;

Q_total = 380.122;

S_original = sqrt( ...
    P_total^2 + Q_total^2);


%% Original Power Factor

PF_original = ...
    P_total / S_original;


%% Target Power Factor

PF_target = 0.95;


%% Angles

phi_initial = acos(PF_original);

phi_target = acos(PF_target);


%% Required Capacitor

Q_required = ...
    P_total * ...
    (tan(phi_initial) - ...
     tan(phi_target));


%% Selected Practical Capacitor

Q_capacitor = 125;


%% New Reactive Power

Q_new = ...
    Q_total - Q_capacitor;


%% New Apparent Power

S_new = sqrt( ...
    P_total^2 + Q_new^2);


%% New Power Factor

PF_new = ...
    P_total / S_new;


%% Current

V = 415;


I_before = ...
    S_original * 1000 / ...
    (sqrt(3) * V);


I_after = ...
    S_new * 1000 / ...
    (sqrt(3) * V);


%% Transformer Loading

transformer_rating = 1000;


loading_before = ...
    S_original / transformer_rating * 100;


loading_after = ...
    S_new / transformer_rating * 100;


%% Current Reduction

current_reduction = ...
    (I_before - I_after) ...
    / I_before * 100;


%% Display Results

fprintf('\nPower Factor Correction\n');
fprintf('-----------------------\n');

fprintf('Original PF = %.3f\n', ...
    PF_original);

fprintf('Target PF = %.3f\n', ...
    PF_target);

fprintf('Required Capacitor = %.2f kVAR\n', ...
    Q_required);

fprintf('Selected Capacitor = %.2f kVAR\n', ...
    Q_capacitor);

fprintf('New Reactive Power = %.2f kVAR\n', ...
    Q_new);

fprintf('New Apparent Power = %.2f kVA\n', ...
    S_new);

fprintf('New PF = %.3f\n', ...
    PF_new);

fprintf('Current Before = %.2f A\n', ...
    I_before);

fprintf('Current After = %.2f A\n', ...
    I_after);

fprintf('Current Reduction = %.2f %%\n', ...
    current_reduction);

fprintf('Loading Before = %.2f %%\n', ...
    loading_before);

fprintf('Loading After = %.2f %%\n', ...
    loading_after);

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

title('Effect of Power Factor Correction');

grid on;

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

yline(100, '--');
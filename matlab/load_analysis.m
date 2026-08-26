clc;
clear;
close all;

% --------------------------------
% System parameters
% --------------------------------

V = 415;

% Load names
load_names = [
    "Motor 1"
    "Motor 2"
    "Pump"
    "Compressor"
    "Auxiliary"
];

% Active power in kW
P_kW = [
    200
    150
    100
    120
    80
];

% Power factor
PF = [
    0.85
    0.82
    0.88
    0.86
    0.95
];


% --------------------------------
% Calculations
% --------------------------------

phi = acos(PF);

Q_kVAR = P_kW .* tan(phi);

S_kVA = sqrt(P_kW.^2 + Q_kVAR.^2);

I_A = (P_kW * 1000)./(sqrt(3) * V .* PF);


% --------------------------------
% Display results
% --------------------------------

results = table(load_names,P_kW,Q_kVAR,S_kVA,PF,I_A);

disp(results);


% --------------------------------
% Total values
% --------------------------------

P_total = sum(P_kW);

Q_total = sum(Q_kVAR);

S_total = sqrt(P_total^2 +Q_total^2);

PF_total = P_total / S_total;

fprintf('\nSystem Totals\n');
fprintf('-------------\n');

fprintf('Total Active Power = %.2f kW\n',P_total);

fprintf('Total Reactive Power = %.2f kVAR\n',Q_total);

fprintf('Total Apparent Power = %.2f kVA\n',S_total);

fprintf('Overall Power Factor = %.3f\n',PF_total);

figure;

bar(P_kW);

xticklabels(load_names);

xlabel('Industrial Load');

ylabel('Active Power (kW)');

title('Active Power Consumption');

grid on;

%% Transformer Parameters

transformer_rating_kVA = 1000;

HV_voltage = 11000;

LV_voltage = 415;

core_loss_kW = 2.5;

copper_loss_rated_kW = 10;


%% Transformer Loading

transformer_loading = ...
    S_total / transformer_rating_kVA;

transformer_loading_percent = ...
    transformer_loading * 100;


%% Transformer Currents

LV_full_load_current = ...
    (transformer_rating_kVA * 1000) / ...
    (sqrt(3) * LV_voltage);

HV_full_load_current = ...
    (transformer_rating_kVA * 1000) / ...
    (sqrt(3) * HV_voltage);

LV_actual_current = ...
    (S_total * 1000) / ...
    (sqrt(3) * LV_voltage);


%% Transformer Losses

copper_loss_kW = ...
    transformer_loading^2 * ...
    copper_loss_rated_kW;

total_loss_kW = ...
    core_loss_kW + copper_loss_kW;


%% Efficiency

transformer_efficiency = ...
    P_total / ...
    (P_total + total_loss_kW) * 100;


%% Display

fprintf('\nTransformer Analysis\n');
fprintf('--------------------\n');

fprintf('Transformer Rating = %.2f kVA\n', ...
    transformer_rating_kVA);

fprintf('Transformer Loading = %.2f %%\n', ...
    transformer_loading_percent);

fprintf('LV Full Load Current = %.2f A\n', ...
    LV_full_load_current);

fprintf('HV Full Load Current = %.2f A\n', ...
    HV_full_load_current);

fprintf('Actual LV Current = %.2f A\n', ...
    LV_actual_current);

fprintf('Copper Loss = %.2f kW\n', ...
    copper_loss_kW);

fprintf('Total Loss = %.2f kW\n', ...
    total_loss_kW);

fprintf('Efficiency = %.2f %%\n', ...
    transformer_efficiency);

figure;

bar([
    S_total
    transformer_rating_kVA
]);

xticklabels({
    'Actual Load'
    'Transformer Rating'
});

ylabel('Apparent Power (kVA)');

title('Transformer Loading');

grid on;

figure;

bar(transformer_loading_percent);

ylim([0 120]);

ylabel('Loading (%)');

title('Transformer Loading Percentage');

yline(100, '--');

grid on;
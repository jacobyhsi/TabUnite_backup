import torch
import numpy as np

from dataset import OnlineToyDataset
from methods.i2bflow.models.modules import MLPDiffusion, Model
from methods.i2bflow.models.flow_matching import ConditionalFlowMatcher
from methods.i2bflow.models.flow_matching import sample as cfm_sampler
from dataset import plot_rings_example, plot_25_gaussian_example, plot_olympic_example

def bits_needed(categories):
    return np.ceil(np.log2(categories)).astype(int)

def get_model(
    model_name,
    model_params,
    n_num_features,
    category_sizes
): 
    print(model_name)
    if model_name == 'mlp':
        model = MLPDiffusion(**model_params)
    else:
        raise "Unknown model!"
    return model

def sample(
    model_save_path,
    dataname,
    steps = 1000,
    lr = 0.002,
    weight_decay = 1e-4,
    batch_size = 1024,
    model_type='mlp',
    model_params = None,
    device=torch.device('cuda:0'),
):
    dataset = OnlineToyDataset(dataname)

    K = np.array(dataset.get_category_sizes())
    num_numerical_features = dataset.get_numerical_sizes()
    num_bits_per_cat_feature = bits_needed(K) if len(K) > 0 else np.array([0])
    d_in = np.sum(num_bits_per_cat_feature) + num_numerical_features
    model_params['d_in'] = d_in

    flow_net = get_model(
        model_type,
        model_params,
        num_numerical_features,
        category_sizes=dataset.get_category_sizes()
    )

    model_path =f'{model_save_path}/model.pt'
    flow_net.load_state_dict(
        torch.load(model_path, map_location="cpu")
    )

    cfm = ConditionalFlowMatcher(sigma=0.0, pred_x1=False)
    model = Model(
        flow_net,
        cfm,
        num_numerical_features,
        K,
        num_bits_per_cat_feature,
    )
    model.to(device)
    model.eval()

    num_samples = 20000

    for step in [2, 5, 10, 30, 50, 100, 300, 500, 1000]:
        x_gen = cfm_sampler(model, num_samples, d_in, N=step, device=device, use_tqdm=True)

        if dataname == 'rings':
            plot_rings_example(x_gen, f'{model_save_path}/rings_i2bflow_steps={step}.png')
        elif dataname == 'olympic':
            plot_olympic_example(x_gen, f'{model_save_path}/olympic_i2bflow_steps={step}.png')
        elif dataname == '25gaussians':
            plot_25_gaussian_example(x_gen, f'{model_save_path}/25gaussians_i2bflow_steps={step}.png')
        else:
            raise "Unknown dataset!"

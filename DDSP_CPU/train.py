# import os
# import argparse
# import torch

# from logger import utils
# from data_loaders import get_data_loaders
# from solver import train
# from ddsp.vocoder import Sins, CombSub, CombSubFast
# from ddsp.loss import RSSLoss


# def parse_args(args=None, namespace=None):
#     """Parse command-line arguments."""
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-c",
#         "--config",
#         type=str,
#         required=True,
#         help="path to the config file")
#     return parser.parse_args(args=args, namespace=namespace)


# if __name__ == '__main__':
#     # parse commands
#     cmd = parse_args()
    
#     # load config
#     args = utils.load_config(cmd.config)
#     print(' > config:', cmd.config)
#     print(' >    exp:', args.env.expdir)

#     # load model
#     model = None
    
#     if args.model.type == 'Sins':
#         model = Sins(
#             sampling_rate=args.data.sampling_rate,
#             block_size=args.data.block_size,
#             n_harmonics=args.model.n_harmonics,
#             n_mag_allpass=args.model.n_mag_allpass,
#             n_mag_noise=args.model.n_mag_noise,
#             n_unit=args.data.encoder_out_channels,
#             n_spk=args.model.n_spk)
 
#     elif args.model.type == 'CombSub':
#         model = CombSub(
#             sampling_rate=args.data.sampling_rate,
#             block_size=args.data.block_size,
#             n_mag_allpass=args.model.n_mag_allpass,
#             n_mag_harmonic=args.model.n_mag_harmonic,
#             n_mag_noise=args.model.n_mag_noise,
#             n_unit=args.data.encoder_out_channels,
#             n_spk=args.model.n_spk)
    
#     elif args.model.type == 'CombSubFast':
#         model = CombSubFast(
#             sampling_rate=args.data.sampling_rate,
#             block_size=args.data.block_size,
#             n_unit=args.data.encoder_out_channels,
#             n_spk=args.model.n_spk)
            
#     else:
#         raise ValueError(f" [x] Unknown Model: {args.model.type}")
    
#     # load parameters
#     optimizer = torch.optim.AdamW(model.parameters())
#     initial_global_step, model, optimizer = utils.load_model(args.env.expdir, model, optimizer, device=args.device)
#     for param_group in optimizer.param_groups:
#         param_group['lr'] = args.train.lr
#         param_group['weight_decay'] = args.train.weight_decay
        
#     # loss
#     loss_func = RSSLoss(args.loss.fft_min, args.loss.fft_max, args.loss.n_scale, device = args.device)

#     # device
#     # if args.device == 'cuda':
#     #     torch.cuda.set_device(args.env.gpu_id)
#     device = 'cpu'
#     args.device = device
#     model.to(args.device)
    
#     for state in optimizer.state.values():
#         for k, v in state.items():
#             if torch.is_tensor(v):
#                 state[k] = v.to(args.device)
                    
#     loss_func.to(args.device)

#     # datas
#     loader_train, loader_valid = get_data_loaders(args, whole_audio=False)
    
#     # run
#     train(args, initial_global_step, model, optimizer, loss_func, loader_train, loader_valid)
    
# def ddsp_train(args):
#     print(' >    exp:', args.env.expdir)

#     # load model
#     model = None
    
#     if args.model.type == 'Sins':
#         model = Sins(
#             sampling_rate=args.data.sampling_rate,
#             block_size=args.data.block_size,
#             n_harmonics=args.model.n_harmonics,
#             n_mag_allpass=args.model.n_mag_allpass,
#             n_mag_noise=args.model.n_mag_noise,
#             n_unit=args.data.encoder_out_channels,
#             n_spk=args.model.n_spk)
 
#     elif args.model.type == 'CombSub':
#         model = CombSub(
#             sampling_rate=args.data.sampling_rate,
#             block_size=args.data.block_size,
#             n_mag_allpass=args.model.n_mag_allpass,
#             n_mag_harmonic=args.model.n_mag_harmonic,
#             n_mag_noise=args.model.n_mag_noise,
#             n_unit=args.data.encoder_out_channels,
#             n_spk=args.model.n_spk)
    
#     elif args.model.type == 'CombSubFast':
#         model = CombSubFast(
#             sampling_rate=args.data.sampling_rate,
#             block_size=args.data.block_size,
#             n_unit=args.data.encoder_out_channels,
#             n_spk=args.model.n_spk)
            
#     else:
#         raise ValueError(f" [x] Unknown Model: {args.model.type}")
    
#     # load parameters
#     optimizer = torch.optim.AdamW(model.parameters())
#     initial_global_step, model, optimizer = utils.load_model(args.env.expdir, model, optimizer, device=args.device)
#     for param_group in optimizer.param_groups:
#         param_group['lr'] = args.train.lr
#         param_group['weight_decay'] = args.train.weight_decay
        
#     # loss
#     loss_func = RSSLoss(args.loss.fft_min, args.loss.fft_max, args.loss.n_scale, device = args.device)

#     # device
#     # if args.device == 'cuda':
#     #     torch.cuda.set_device(args.env.gpu_id)
#     device = 'cpu'
#     args.device = device
#     model.to(args.device)
    
#     for state in optimizer.state.values():
#         for k, v in state.items():
#             if torch.is_tensor(v):
#                 state[k] = v.to(args.device)
                    
#     loss_func.to(args.device)

#     # datas
#     loader_train, loader_valid = get_data_loaders(args, whole_audio=False)
    
#     # run
#     train(args, initial_global_step, model, optimizer, loss_func, loader_train, loader_valid)

#     # Save the trained model
#     model_last_path = os.path.join('exp/combsub-test', 'model_last.pt')
#     torch.save({
#         'model_state_dict': model.state_dict(),
#         'optimizer_state_dict': optimizer.state_dict(),
#         'global_step': initial_global_step
#     }, model_last_path)

#     print(f" [+] Trained model saved at: {model_last_path}")


import os
import argparse
import torch
import signal
import sys

from logger import utils
from data_loaders import get_data_loaders
from solver import train
from ddsp.vocoder import Sins, CombSub, CombSubFast
from ddsp.loss import RSSLoss


def parse_args(args=None, namespace=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help="path to the config file")
    return parser.parse_args(args=args, namespace=namespace)

def save_model_on_interrupt(model, optimizer, global_step, model_path):
    def signal_handler(signal, frame):
        print("\n [!] Ctrl+C pressed. Saving the model...")
        torch.save({
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'global_step': global_step
        }, model_path)
        print(f" [+] Trained model saved at: {model_path}")
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    # parse commands
    cmd = parse_args()
    
    # load config
    args = utils.load_config(cmd.config)
    print(' > config:', cmd.config)
    print(' >    exp:', args.env.expdir)

    # load model
    model = None
    
    if args.model.type == 'Sins':
        model = Sins(
            sampling_rate=args.data.sampling_rate,
            block_size=args.data.block_size,
            n_harmonics=args.model.n_harmonics,
            n_mag_allpass=args.model.n_mag_allpass,
            n_mag_noise=args.model.n_mag_noise,
            n_unit=args.data.encoder_out_channels,
            n_spk=args.model.n_spk)
 
    elif args.model.type == 'CombSub':
        model = CombSub(
            sampling_rate=args.data.sampling_rate,
            block_size=args.data.block_size,
            n_mag_allpass=args.model.n_mag_allpass,
            n_mag_harmonic=args.model.n_mag_harmonic,
            n_mag_noise=args.model.n_mag_noise,
            n_unit=args.data.encoder_out_channels,
            n_spk=args.model.n_spk)
    
    elif args.model.type == 'CombSubFast':
        model = CombSubFast(
            sampling_rate=args.data.sampling_rate,
            block_size=args.data.block_size,
            n_unit=args.data.encoder_out_channels,
            n_spk=args.model.n_spk)
            
    else:
        raise ValueError(f" [x] Unknown Model: {args.model.type}")
    
    # load parameters
    optimizer = torch.optim.AdamW(model.parameters())
    initial_global_step, model, optimizer = utils.load_model(args.env.expdir, model, optimizer, device=args.device)
    for param_group in optimizer.param_groups:
        param_group['lr'] = args.train.lr
        param_group['weight_decay'] = args.train.weight_decay
        
    # loss
    loss_func = RSSLoss(args.loss.fft_min, args.loss.fft_max, args.loss.n_scale, device = args.device)

    # device
    # if args.device == 'cuda':
    #     torch.cuda.set_device(args.env.gpu_id)
    device = 'cpu'
    args.device = device
    model.to(args.device)
    
    for state in optimizer.state.values():
        for k, v in state.items():
            if torch.is_tensor(v):
                state[k] = v.to(args.device)
                    
    loss_func.to(args.device)

    # datas
    loader_train, loader_valid = get_data_loaders(args, whole_audio=False)
    
    # run
    train(args, initial_global_step, model, optimizer, loss_func, loader_train, loader_valid)
    
def ddsp_train(args):
    print(' >    exp:', args.env.expdir)

    # load model
    model = None
    
    if args.model.type == 'Sins':
        model = Sins(
            sampling_rate=args.data.sampling_rate,
            block_size=args.data.block_size,
            n_harmonics=args.model.n_harmonics,
            n_mag_allpass=args.model.n_mag_allpass,
            n_mag_noise=args.model.n_mag_noise,
            n_unit=args.data.encoder_out_channels,
            n_spk=args.model.n_spk)
 
    elif args.model.type == 'CombSub':
        model = CombSub(
            sampling_rate=args.data.sampling_rate,
            block_size=args.data.block_size,
            n_mag_allpass=args.model.n_mag_allpass,
            n_mag_harmonic=args.model.n_mag_harmonic,
            n_mag_noise=args.model.n_mag_noise,
            n_unit=args.data.encoder_out_channels,
            n_spk=args.model.n_spk)
    
    elif args.model.type == 'CombSubFast':
        model = CombSubFast(
            sampling_rate=args.data.sampling_rate,
            block_size=args.data.block_size,
            n_unit=args.data.encoder_out_channels,
            n_spk=args.model.n_spk)
            
    else:
        raise ValueError(f" [x] Unknown Model: {args.model.type}")
    
    # load parameters
    optimizer = torch.optim.AdamW(model.parameters())
    initial_global_step, model, optimizer = utils.load_model(args.env.expdir, model, optimizer, device=args.device)
    for param_group in optimizer.param_groups:
        param_group['lr'] = args.train.lr
        param_group['weight_decay'] = args.train.weight_decay
        
    # loss
    loss_func = RSSLoss(args.loss.fft_min, args.loss.fft_max, args.loss.n_scale, device = args.device)

    # device
    # if args.device == 'cuda':
    #     torch.cuda.set_device(args.env.gpu_id)
    device = 'cpu'
    args.device = device
    model.to(args.device)
    
    for state in optimizer.state.values():
        for k, v in state.items():
            if torch.is_tensor(v):
                state[k] = v.to(args.device)
                    
    loss_func.to(args.device)

    # datas
    loader_train, loader_valid = get_data_loaders(args, whole_audio=False)

    # Define model_last_path before registering the signal handler
    model_last_path = os.path.join('exp/combsub-test', 'model_last.pt')

    # Register the signal handler for saving the model on KeyboardInterrupt
    save_model_on_interrupt(model, optimizer, initial_global_step, model_last_path)

    # run
    train(args, initial_global_step, model, optimizer, loss_func, loader_train, loader_valid)

    # Save the trained model
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'global_step': initial_global_step
    }, model_last_path)

    print(f" [+] Trained model saved at: {model_last_path}")
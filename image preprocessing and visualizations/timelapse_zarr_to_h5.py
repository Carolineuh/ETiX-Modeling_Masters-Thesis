#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimalist command line program for compression of OME-Zarr to H5.
"""

def main():
    CLI = argparse.ArgumentParser()
    CLI.add_argument('idx', type=int)
    CLI.add_argument('fld', type=str)
    CLI.add_argument("--out_fld", type=str)
    args = CLI.parse_args()

    args.out_fld.mkdir(exist_ok=True)

    fns = sorted(list(Path(args.fld).glob('*.zarr')))

    fn = fns[args.idx]

    def convert_zarr_to_h5(fn, args.out_fld, level=3):
        write_h5_file(fn, args.out_fld, level)

        def write_h5_file(fn, out_fld, level):
            output_fn = out_fld / (fn.stem + '.h5') 

            f = zarr.open(fn, mode='r')
            fn_in = f[level][...] 

            dsets = {}
            for idx, f in enumerate(np.rollaxis(fn_in, 1)):
                dset = []
                for tp in f:
                    dset.append(np.max(tp, axis=0)) # convert stack to max projection
                dsets[f"ch_0{idx}"] = dset

            with h5py.File(output_fn, 'a') as f_out: # write to new h5 file
                for k,v in dsets.items():
                    f_out.create_dataset(k, data=v)
                    dset = f_out[k]
                    dset.attrs['element_size_um'] = [3, 2.6, 2.6] # pixel size of z, y, x - adjust if using a different level than 3

    convert_zarr_to_h5(fn)
  
if __name__ == "__main__":
    main()
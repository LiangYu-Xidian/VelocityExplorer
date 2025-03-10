import matplotlib.pyplot as plt
import scanpy as sc
import scanpy.external as sce
import scvelo as scv
import sys


if __name__ == '__main__':


    file_path = sys.argv[1]
    clustersIndex = sys.argv[2]
    # 将sys.argv[3]和sys.argv[4]按';'分割, 并将分割后的结果存入method_list和mode_list中
    method_list = sys.argv[3].split(';')
    mode_list = sys.argv[4].split(';')

    adata_list = []
    adata = scv.read(file_path, cache=True)
    sc.pp.subsample(adata, n_obs=1000)
    scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=2000)
    scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

    # 当clustersIndex不在adata.obs.keys()中时, 将clustersIndex赋值为None
    if clustersIndex not in adata.obs.keys():
        clustersIndex = None

    if 'umap' in method_list:
        sc.tl.umap(adata)
    if 'pca' in method_list:
        sc.tl.pca(adata)
    if 'tsne' in method_list:
        sc.tl.tsne(adata)
    if 'phate' in method_list:
        sce.tl.phate(adata)
    if 'diffmap' in method_list:
        sc.tl.diffmap(adata, n_comps=3)

    adata_bak = adata.copy()

    for mode in mode_list:
        adata = adata_bak.copy()
        if mode == 'dynamical':
            scv.tl.recover_dynamics(adata, n_jobs=4)
        scv.tl.velocity(adata, mode=mode)
        adata_list.append(adata)

    rows = len(adata_list)  # 与模式一一对应
    cols = len(method_list)
    fig, ax = plt.subplots(rows, cols, figsize=(15, 12))

    for i in range(rows):
        adata = adata_list[i]
        mode = mode_list[i]
        scv.tl.velocity_graph(adata)
        for j in range(cols):
            basis = method_list[j]
            title = "%s_%s" % (mode, basis)
            if i == rows - 1 and j == cols - 1:
                if rows == 1 and cols == 1:
                    scv.pl.velocity_embedding_stream(adata, basis=basis, ax=ax, title=title, color=clustersIndex, show=False,
                                                     save='stream.png')
                elif rows == 1:
                    scv.pl.velocity_embedding_stream(adata, basis=basis, ax=ax[j], title=title, color=clustersIndex, show=False,
                                                     save='stream.png')
                elif cols == 1:
                    scv.pl.velocity_embedding_stream(adata, basis=basis, ax=ax[i], title=title, color=clustersIndex, show=False,
                                                     save='stream.png')
                else:
                    scv.pl.velocity_embedding_stream(adata, basis=basis, ax=ax[i][j], title=title, color=clustersIndex, show=False,
                                                 save='stream.png')
            else:
                if rows == 1 and cols == 1:
                    scv.pl.velocity_embedding_stream(adata, basis=basis, ax=ax, title=title, color=clustersIndex, show=False)
                elif rows == 1:
                    scv.pl.velocity_embedding_stream(adata, basis=basis, ax=ax[j], title=title, color=clustersIndex, show=False)
                elif cols == 1:
                    scv.pl.velocity_embedding_stream(adata, basis=basis, ax=ax[i], title=title, color=clustersIndex, show=False)
                else:
                    scv.pl.velocity_embedding_stream(adata, basis=basis, ax=ax[i][j], title=title, color=clustersIndex, show=False)


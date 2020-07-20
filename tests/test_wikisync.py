# from igem_wikisync import wikisync

# import filecmp

# def test_wikisync():

#     wikisync.run()

#     team = 'BITSPilani-Goa_India'
#     src_dir = 'test_src'
#     build_dir = 'test_build'
#     assets = ['assets']

#     wikisync(
#         team=team,
#         src_dir=src_dir,
#         build_dir=build_dir,
#         assets=assets)

#     with open('test_build/index.html', 'r') as outfile:
#         with open('test_ref/index.html', 'r') as reference:

#             assert filecmp.cmp(outfile, reference)
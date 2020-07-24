# from igem_wikisync import wikisync

# # import filecmp

# def test_wikisync():

#     team = 'BITSPilani-Goa_India'
#     src_dir = 'tests/data'
#     build_dir = 'tests/build'
#     # assets = ['assets']

#     wikisync.run(
#         team=team,
#         src_dir=src_dir,
#         build_dir=build_dir)

#     with open('test_build/index.html', 'r') as outfile:
#         with open('test_ref/index.html', 'r') as reference:

#             assert filecmp.cmp(outfile, reference)
__author__ = 'xiaolisong'


class pattern_mining():

    def __init__(self, list):
        self.list = list

    def __sa(self):
        sa_unsorted = []
        for doc_id in range(0,len(self.list)):
            sentence = self.list[doc_id]
            for start in range(0,len(sentence)):
                if start == 0 or (start != 0 and sentence[start-1] == ' '):
                    suffix = sentence[start:]
                    suffix_with_index = (suffix,(doc_id, start))
                    sa_unsorted.append(suffix_with_index)

        sa_unsorted.sort(lambda x, y: cmp(x, y))
        sa = {}

        for i in range(0, len(sa_unsorted)):
            sa[i] = sa_unsorted[i][1]

        return sa

    def __spc_lcp(self, sa, threshold):
        spc_lcp = {}
        for i in range(0, len(sa)-threshold+1):
            lcp = self.list[sa[i][0]][sa[i][1]:]
            for j in range(i+1,i+threshold):
                suffix = self.list[sa[j][0]][sa[j][1]:]
                lcp = self.__calculate_lcp(lcp, suffix)
            lcp_len = len(lcp)
            if lcp_len != 0:
                if lcp in spc_lcp:
                    for k in range(i,i+threshold):
                        position_length = sa[k]+(lcp_len,)
                        spc_lcp[lcp].add(position_length)
                else:
                    spc_lcp[lcp] = set([])
                    for k in range(i, i+threshold):
                        position_length = sa[k]+(lcp_len,)
                        spc_lcp[lcp].add(position_length)
        return spc_lcp

    def __calculate_lcp(self, lcp_each, suffix):
        words1 = lcp_each.split()
        words2 = suffix.split()
        prefix = ''
        max_common = min(len(words1), len(words2))
        for i in range(0,max_common):
            if words1[i] == words2[i]:
                prefix += ' '+words1[i]
            else:
                break
        prefix = prefix.strip()
        return prefix

    def __espc(self, spc_lcp, threshold):
        count_remove = 0
        espc = {}
        mapping_patternid_pattern = {}
        mapping_position_patternnum = {}
        index = 0
        for pattern in spc_lcp:
            positions = spc_lcp[pattern]
            mapping_patternid_pattern[index] = pattern
            for position in positions:
                mapping_position_patternnum[position] = index
            index += 1
        positions_all = mapping_position_patternnum.keys()
        for position in positions_all:
            doc_id = position[0]
            start_id = position[1]
            length_p = position[2]
            for start in range(start_id+1,start_id+length_p):
                for length in range(1,length_p-start+start_id+1):
                    subset_p = (doc_id,start,length)
                    if subset_p in mapping_position_patternnum:
                        if subset_p in spc_lcp[mapping_patternid_pattern[mapping_position_patternnum[subset_p]]]:
                            if self.list[doc_id][start_id:start_id+length_p] != self.list[doc_id][start:start+length]:
                                count_remove += 1
                                spc_lcp[mapping_patternid_pattern[mapping_position_patternnum[subset_p]]].remove(subset_p)

        for pattern in spc_lcp:
            if len(spc_lcp[pattern]) >= threshold:
                espc[pattern] = spc_lcp[pattern]
        return espc

    def run(self, threshold):
        sa = self.__sa()
        spc_lcp = self.__spc_lcp(sa, threshold)
        espc = self.__espc(spc_lcp,threshold)
        return espc



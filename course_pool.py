#!/usr/bin/env python
# encoding: utf-8

# 课程池，用于处理各种有关课程的操作

import configure as cfg
from course_table import CourseTable
import debug

d = debug.Debug('course_pool')

class CoursePool:
    #------ 对外接口 ------
    def id_to_course(self, courseid):
        return self._courseid_course_dict[courseid]

    def course_to_table(self, courseid):
        return self._courseid_table_dict[courseid]

    def find_max_course_num(self, tables):
        return max(tables, key=lambda x: x.get_course_num())

    def get_eachday_course(self, table):
        return table.eachday_course

    def get_teacher_courseids(self, t):
        return self._teacher_cid_dict[t]

    def get_sorted_courses(self):
        return self._sorted_course

    def get_detail_tables(self):
        result = []
        for table in self._tables:
            result.append('GRUOP: %s' % table.title)
            result.append(self._table_detail(table.table))
        return '\n'.join(result)

    #----基本方法
    def __init__(self, all_courses):
        # 所有的课程
        self._all_courses = all_courses
        # 每个courseid对应的课程
        self._courseid_course_dict = self._get_courseid_course_dict()
        # 所有group的课程表
        self._tables = self._get_all_tables()
        # group 对应的课程表
        self._group_table_dict = self._get_group_table_dict()
        # 每个课程对应的课程表
        self._courseid_table_dict = self._get_courseid_table_dict()
        # 每个老师教的所有课程id
        self._teacher_cid_dict = self._get_teacher_cid_dict()
        self._sorted_course = self._sort_course()

    def _sort_course(self):
        """对所有的课程进行排序

        对于有要求的课
        1. 上同一门课的班级越多，这门课最靠前（因为涉及到了不同的课表）
        2. 一门课老师要求越多（比如除了每天时间限制之外，还有星期的限制），越靠前
        3. 对于有相同多要求的，要求范围越窄越靠前
        """
        # TODO
        return self._all_courses



    def _get_teacher_cid_dict(self):
        tcd = {}
        for c in self._all_courses:
            for t in c.teachers:
                try:
                    if c.cid not in tcd[t]:
                        tcd[t].append(c.cid)
                except KeyError:
                    tcd[t] = [c.cid]
        return tcd

    def _get_courseid_course_dict(self):
        ccd = {}
        for c in self._all_courses:
            ccd[c.cid] = c
        return ccd

    def _get_group_table_dict(self):
        "每个 group 对应一个 table"
        gtd = {}
        for table in self._tables:
            gtd[table.title] = table
        return gtd

    def _get_all_groups(self):
        "得到所有的group名字"
        groups = []
        for c in self._all_courses:
            groups.extend(c.groups)
        return set(groups)

    def _get_courseid_table_dict(self):
        """返回课程与课程对应的group的table"""
        ctd = {}
        for c in self._all_courses:
            for g in c.groups:
                try:
                    # 去重，因为在 _all_courses 里面可能会出现两个
                    # 一样的课程（e.g.一个星期上两次2次2学分的X课）
                    if self._group_table_dict[g] not in ctd[c.cid]:
                        ctd[c.cid].append(self._group_table_dict[g])
                except KeyError:
                    ctd[c.cid] = [self._group_table_dict[g]]
        return ctd

    def _get_all_tables(self):
        #得到年级与相应课程的映射
        groups = self._get_all_groups()

        # 初始化课程表
        tables = []
        for k in groups:
            tables.append(CourseTable(k))
        return tables

    def _table_detail(self, num_table):
        "返回课程表具体内容"
        s = ""
        for i in xrange(len(cfg.TIME)):
            s += cfg.TIME[i] + ' '
            for j in range(len(cfg.DAY)):
                cid = num_table[i][j]
                if cid == -1:
                    s += '_'*15
                else:
                    s += (self.id_to_course(cid).name+"_"*15)[:15]
                s += '  '
            s += '\n'
        return s



if __name__ == '__main__':
    import reader
    r = reader.Reader('test.csv')
    cp = CoursePool(r.courses)
    # 打印所有的课程
    for c in cp._all_courses:
        print c.cid, c.name, c.credit, c.groups, c.teachers

    print 'ALL GROUPS: %s' % cp._get_all_groups()

    print '============='
    for i in cp._tables:
        print i
    print '-------------'
    for i in cp._group_table_dict:
        print 'GROUP: %s' % i
        print cp._group_table_dict[i]
    print '每个课程对应的课程表：'
    for i in cp._courseid_table_dict:
        c = cp.id_to_course(i)
        print 'COURSE: %s %s %s' % (c.name, c.groups, c.teachers)
        for k in cp._courseid_table_dict[i]:
            print k
    print '每个老师对应的课程'
    for t in cp._teacher_cid_dict:
        print 'TEACHER: %s' % t
        print cp._teacher_cid_dict[t]
